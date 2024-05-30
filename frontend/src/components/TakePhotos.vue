<template>
  <div class="container mt-3 mt-md-5">
    <div class="card mx-auto" :class="cardClass">
      <div class="card-body text-center">
        <h5 class="card-title">Take Photos</h5>
        <div v-if="cameraStream" class="camera-container mt-3">
          <video ref="camera" autoplay playsinline></video>
          <button class="btn btn-secondary mt-2" @click="takePhoto">Capture Photo</button>
          <div class="mt-3">
            <h6>Captured Photos:</h6>
            <div v-for="(src, index) in previews" :key="index" class="preview">
              <img :src="src" alt="preview" class="img-thumbnail">
            </div>
          </div>
        </div>
        <button class="btn btn-primary mt-3 w-100" @click="processPhotos">Process</button>
      </div>
    </div>
  </div>
</template>

<script>
import { nextTick } from 'vue';

export default {
  data() {
    return {
      previews: [],
      cameraStream: null
    };
  },
  computed: {
    cardClass() {
      return {
        'w-100': true,
        'w-md-50': true
      };
    }
  },
  mounted() {
    this.openCamera();
  },
  beforeUnmount() {
    this.closeCamera();
  },
  methods: {
    async openCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        this.cameraStream = stream;
        await nextTick();
        this.$refs.camera.srcObject = stream;
      } catch (err) {
        console.error("Error accessing camera: ", err);
      }
    },
    takePhoto() {
      const video = this.$refs.camera;
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      const imgData = canvas.toDataURL('image/png');
      this.previews.push(imgData);
    },
    closeCamera() {
      if (this.cameraStream) {
        this.cameraStream.getTracks().forEach(track => track.stop());
        this.cameraStream = null;
      }
    },
    processPhotos() {
      // Implement photo processing logic
      console.log("Processing photos:", this.previews);
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 100%;
  padding-left: 15px;
  padding-right: 15px;
}
.card {
  border-radius: 10px;
}
.card-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 3rem;
}
.preview {
  margin: 5px;
}
.camera-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}
video {
  width: 100%;
  height: auto;
  border-radius: 10px;
}
@media (min-width: 768px) {
  .card {
    max-width: 400px;
  }
}
</style>
