<template>
  <div class="container mt-3 mt-md-5">
    <div class="card mx-auto">
      <div class="card-body text-center">
        <h5 class="card-title">Take Photos</h5>
        <div class="video-container" v-show="!isLoading">
          <video ref="video" autoplay playsinline></video>
          <button @click="takePhoto" class="camera-button"></button>
          <button @click="toggleCamera" class="switch-button">
            <i class="bi bi-arrow-repeat"></i>
          </button>
        </div>
        <div class="file-previews-container">
          <div v-for="(photo, index) in photos" :key="index" class="photo-preview">
            <img :src="photo" class="img-thumbnail" />
            <button @click="removePhoto(index)" class="btn btn-danger btn-sm" :disabled="isLoading">
              <i class="fas fa-times"></i>
            </button>
          </div>
        </div>
        <button class="btn btn-primary mt-3 w-100" @click="processPhotos" :disabled="!isValid || isLoading">
          <i v-if="isLoading" class="fas fa-spinner fa-spin"></i>
          <span v-else>
            <i class="fas fa-cogs"></i>
            Process</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      photos: [],
      isLoading: false,
      facingMode: 'environment', // or 'user' for front camera
    };
  },
  computed: {
    isValid() {
      return this.photos.length > 0;
    },
  },
  mounted() {
    this.initCamera();
  },
  methods: {
    async initCamera() {
      try {
        const constraints = {
          video: {
            facingMode: this.facingMode,
          },
        };
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        this.$refs.video.srcObject = stream;
      } catch (error) {
        console.error("Error accessing camera:", error);
      }
    },
    takePhoto() {
      const canvas = document.createElement("canvas");
      canvas.width = this.$refs.video.videoWidth;
      canvas.height = this.$refs.video.videoHeight;
      canvas.getContext("2d").drawImage(this.$refs.video, 0, 0);
      this.photos.push(canvas.toDataURL("image/png"));
    },
    removePhoto(index) {
      this.photos.splice(index, 1);
    },
    async processPhotos() {
      this.isLoading = true;
      try {
        const formData = new FormData();
        this.photos.forEach((photo, index) => {
          const blob = this.dataURLtoBlob(photo);
          formData.append("files", new File([blob], `photo${index}.png`));
        });

        const objectName = this.$store.state.global.formData.objectName;
        formData.append("objectName", objectName);

        await axios.post(`${process.env.VITE_API_URL}/upload`, formData);
        console.log("Uploaded photos");
        this.$router.push("/model-view");
      } catch (error) {
        console.error("Error uploading photos:", error);
        console.error("Server response:", error.response);
      } finally {
        this.isLoading = false;
      }
    },
    dataURLtoBlob(dataURL) {
      const byteString = atob(dataURL.split(",")[1]);
      const mimeString = dataURL.split(",")[0].split(":")[1].split(";")[0];
      const buffer = new ArrayBuffer(byteString.length);
      const data = new DataView(buffer);
      for (let i = 0; i < byteString.length; i++) {
        data.setUint8(i, byteString.charCodeAt(i));
      }
      return new Blob([buffer], { type: mimeString });
    },
    async toggleCamera() {
      this.facingMode = this.facingMode === 'user' ? 'environment' : 'user';
      const stream = this.$refs.video.srcObject;
      const tracks = stream.getTracks();
      tracks.forEach(track => track.stop());
      await this.initCamera();
    },
  },
};
</script>

<style scoped>
.card {
  width: 310px;
}
.video-container {
  position: relative;
}
.video-container video {
  width: 100%;
}
.camera-button {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  height: 30px;
  background-color: white;
  border: 5px solid rgba(0, 0, 0, 0.2);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 8.5px;
  color: black;
  z-index: 10;
  cursor: pointer;
}
.switch-button {
  position: absolute;
  bottom: 12px;
  right: 0%;
  transform: translateX(-50%);
  height: 25px;
  width: 10px; 
  background-color: rgba(0, 0, 0, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 10px;
  z-index: 10;
  cursor: pointer;
}
.switch-button i {
  font-size: 15px;
}

.file-previews-container {
  max-height: 200px;
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  justify-content: space-evenly;
  margin-top: 10px;
  overflow: scroll;
}
.photo-preview {
  position: relative;
  width: 45%;
}
.img-thumbnail {
  width: 100%;
  height: auto;
}
.btn-danger {
  position: absolute;
  top: -5px;
  right: -2px;
  background-color: transparent;
  border: none;
  font-size: 16px;
}
</style>
