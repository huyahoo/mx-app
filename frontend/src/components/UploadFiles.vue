<template>
  <div class="container mt-3 mt-md-5">
    <div class="card mx-auto" :class="cardClass">
      <div class="card-body text-center">
        <h5 class="card-title">Upload Files</h5>
        <input type="file" ref="fileInput" class="form-control" @change="handleFileUpload" multiple accept="image/*">
        <div v-if="files.length" class="mt-3">
          <h6>Uploaded Files:</h6>
          <ul>
            <li v-for="(file, index) in files" :key="index">{{ file.name }}</li>
          </ul>
        </div>
        <button class="btn btn-primary mt-3 w-100" @click="processFiles">Process</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      files: []
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
    handleFileUpload(event) {
      this.files = Array.from(event.target.files);
    },
    processFiles() {
      // Implement file processing logic
      console.log("Processing files:", this.files);
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
