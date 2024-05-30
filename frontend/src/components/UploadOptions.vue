<template>
  <div class="container mt-3 mt-md-5">
    <div class="card mx-auto" :class="cardClass">
      <div class="card-body text-center">
        <h5 class="card-title">Upload</h5>
        <button class="btn btn-primary my-3 w-100" @click="goToUploadFiles">Upload Files</button>
        <p>Or</p>
        <button class="btn btn-primary my-3 w-100" @click="goToTakePhotos">Take Photos</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    cardClass() {
      return {
        'w-100': true,
        'w-md-50': true
      };
    }
  },
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
.card-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 3rem;
}
@media (min-width: 768px) {
  .card {
    max-width: 400px;
  }
}
</style>
