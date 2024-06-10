<template>
  <div class="container mt-3 mt-md-5">
    <div class="card mx-auto w-100">
      <div class="card-body text-center">
        <h5 class="card-title">Take Photos</h5>
        <div class="video-container">
          <video ref="video" autoplay playsinline></video>
          <button
            @click="takePhoto"
            class="btn btn-primary mt-3 w-100"
          >
            <i
              v-if="isLoading"
              class="fas fa-spinner fa-spin"
            ></i>
            <span v-else>Take Photo</span>
          </button>
        </div>
        <div
          v-for="(photo, index) in photos"
          :key="index"
          class="photo-preview"
        >
          <img :src="photo" class="img-thumbnail" />
          <button
            @click="removePhoto(index)"
            class="btn btn-danger btn-sm"
          >
            <i class="fas fa-times"></i>
          </button>
        </div>
        <button
          class="btn btn-primary mt-3 w-100"
          @click="processPhotos"
        >
          <i
            v-if="isLoading"
            class="fas fa-spinner fa-spin"
          ></i>
          <span v-else>Process</span>
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
    };
  },
  methods: {
    async mounted() {
      const constraints = {
        video: true,
      };
      const stream =
        await navigator.mediaDevices.getUserMedia(
          constraints
        );
      this.$refs.video.srcObject = stream;
    },
    takePhoto() {
      const canvas = document.createElement("canvas");
      canvas.width = this.$refs.video.videoWidth;
      canvas.height = this.$refs.video.videoHeight;
      canvas
        .getContext("2d")
        .drawImage(this.$refs.video, 0, 0);
      this.photos.push(canvas.toDataURL("image/png"));
    },
    removePhoto(index) {
      this.photos.splice(index, 1);
    },
    async processPhotos() {
      this.isLoading = true;
      try {
        const formData = new FormData();
        this.photos.forEach((photo) =>
          formData.append("photos", photo)
        );
        // Use the environment variable
        await axios.post(
          `${process.env.VITE_API_URL}/upload`,
          formData
        );
        console.log("Uploaded photos");
        // Navigate to next screen after successful upload
        this.$router.push("/model-view");
      } catch (error) {
        console.error("Error uploading photos:", error);
      } finally {
        this.isLoading = false;
      }
    },
    dataURLtoBlob(dataURL) {
      const byteString = atob(dataURL.split(",")[1]);
      const mimeString = dataURL
        .split(",")[0]
        .split(":")[1]
        .split(";")[0];
      const buffer = new ArrayBuffer(byteString.length);
      const data = new DataView(buffer);
      for (let i = 0; i < byteString.length; i++) {
        data.setUint8(i, byteString.charCodeAt(i));
      }
      return new Blob([buffer], { type: mimeString });
    },
  },
};
</script>

<style scoped>
.video-container {
  position: relative;
}
.video-container video {
  width: 100%;
}
.photo-preview {
  position: relative;
  margin-top: 10px;
}
.img-thumbnail {
  width: 100%;
  height: auto;
}
.btn-danger {
  position: absolute;
  top: 5px;
  right: 5px;
}
</style>
