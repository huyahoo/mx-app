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
            <div v-for="(src, index) in previews" :key="index" class="preview-container">
              <img :src="src" alt="preview" class="img-thumbnail">
              <button class="btn btn-danger btn-sm remove-btn" @click="removePhoto(index)">x</button>
            </div>
          </div>
        </div>
        <button class="btn btn-primary mt-3 w-100" @click="uploadPhotos">Process</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

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
        await this.$nextTick();
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
    removePhoto(index) {
      this.previews.splice(index, 1);
    },
    closeCamera() {
      if (this.cameraStream) {
        this.cameraStream.getTracks().forEach(track => track.stop());
        this.cameraStream = null;
      }
    },
    async uploadPhotos() {
      const formData = new FormData();
      this.previews.forEach((preview, index) => {
        const byteString = atob(preview.split(',')[1]);
        const mimeString = preview.split(',')[0].split(':')[1].split(';')[0];
        const arrayBuffer = new ArrayBuffer(byteString.length);
        const uint8Array = new Uint8Array(arrayBuffer);
        for (let i = 0; i < byteString.length; i++) {
          uint8Array[i] = byteString.charCodeAt(i);
        }
        const blob = new Blob([arrayBuffer], { type: mimeString });
        formData.append('files', blob, `photo-${index}.png`);
      });

      try {
        const response = await axios.post('http://localhost:5000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('Photos uploaded successfully:', response.data.file_urls);
      } catch (error) {
        console.error('Error uploading photos:', error);
      }
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
  font-size: 1.5rem;
  font-weight: bold;
}
.preview-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px;
}
.img-thumbnail {
  max-width: 100px;
  max-height: 100px;
  margin-bottom: 5px;
}
.remove-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: red;
  border: none;
  color: white;
  font-size: 1rem;
  line-height: 1rem;
  padding: 0.2rem;
  border-radius: 50%;
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
