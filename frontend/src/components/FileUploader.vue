<template>
  <div class="container mt-3 mt-md-5">
    <div class="card mx-auto" :class="cardClass">
      <div class="card-body text-center">
        <h5 class="card-title">Upload</h5>
        <button class="btn btn-primary my-3 w-100" @click="triggerFileInput">Upload Files</button>
        <p>Or</p>
        <button class="btn btn-primary my-3 w-100" @click="openCamera">Take Photos</button>
        <input type="file" ref="fileInput" class="d-none" @change="handleFileUpload" multiple accept="image/*">
        <div v-if="previews.length" class="preview-container mt-3">
          <div v-for="(src, index) in previews" :key="index" class="preview">
            <img :src="src" alt="preview" class="img-thumbnail">
          </div>
        </div>
        <div v-if="cameraStream" class="camera-container mt-3">
          <video ref="camera" autoplay></video>
          <button class="btn btn-secondary mt-2" @click="takePhoto">Capture Photo</button>
          <button class="btn btn-danger mt-2" @click="closeCamera">Close Camera</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
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
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      const files = event.target.files;
      for (let i = 0; i < files.length; i++) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.previews.push(e.target.result);
        };
        reader.readAsDataURL(files[i]);
      }
    },
    openCamera() {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          this.cameraStream = stream;
          this.$refs.camera.srcObject = stream;
        })
        .catch(err => {
          console.error("Error accessing camera: ", err);
        });
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
      this.cameraStream.getTracks().forEach(track => track.stop());
      this.cameraStream = null;
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
.preview-container {
  display: flex;
  flex-wrap: wrap;
}
.preview {
  margin: 5px;
}
.camera-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
@media (min-width: 768px) {
  .card {
    max-width: 400px;
  }
}
</style>
