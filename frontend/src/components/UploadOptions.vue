<template>
  <div class="container mt-3 mt-md-5">
    <div class="card mx-auto">
      <div class="card-body text-center">
        <h5 class="card-title">Upload</h5>
        <button class="btn btn-primary my-3 w-100" @click="goToUploadFiles">
          <i class="bi bi-cloud-upload-fill me-1" style="font-size: 16px"></i>
          Upload Files
        </button>
        <p>Or</p>
        <button class="btn btn-primary my-3 w-100" @click="goToTakePhotos">
          <i class="bi bi-camera-fill me-1"></i>
          Take Photos
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    goToUploadFiles() {
      this.$router.push('/upload-files');
    },
    goToTakePhotos() {
      this.$router.push('/take-photos');
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
@media (min-width: 768px) {
  .card {
    max-width: 400px;
  }
}
</style>
