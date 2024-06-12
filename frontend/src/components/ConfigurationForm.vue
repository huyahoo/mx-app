<template>
  <div class="container mt-md-5">
    <div class="card mx-auto">
      <div class="card-body">
        <h5 class="card-title text-center">Configuration</h5>
        <form @submit.prevent="handleSubmit">
          <div class="mb-3 label__input">
            <label for="objectName" class="form-label">
              Object Name
            </label>
            <input type="text" class="form-control" id="objectName" v-model="formData.objectName">
          </div>
          <div class="mb-3 label__input">
            <label for="saveDestination" class="form-label">Save Destination</label>
            <input type="text" class="form-control" id="saveDestination" v-model="formData.saveDestination" disabled>
          </div>
          <div class="mb-3 label__input">
            <label for="model" class="form-label">Model</label>
            <select class="form-select" id="model" v-model="formData.model">
              <option>Dust3r</option>
              <!-- Add more options as needed -->
            </select>
          </div>
          <button type="submit" class="btn btn-primary w-100" :disabled="isFormInvalid">Next</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    formData () {
      return this.$store.state.global.formData;
    },
    isFormInvalid() {
      return !this.formData.objectName || !this.formData.saveDestination || !this.formData.model;
    }
  },
  methods: {
    handleSubmit() {
      // Handle form submission and navigation
      console.log(this.formData);
      this.$router.push('/upload-options');
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
  width: 310px;
}
@media (min-width: 768px) {
  .card {
    max-width: 400px;
  }
}
</style>
