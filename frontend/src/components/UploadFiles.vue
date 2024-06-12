<template>
  <div class="container mt-3 mt-md-5">
    <div class="card mx-auto w-100">
      <div class="card-body text-center">
        <h5 class="card-title">Upload Files</h5>
        <input
          type="file"
          multiple
          @change="handleFileSelect"
          class="form-control"
        />
        <div
          v-for="(file, index) in files"
          :key="index"
          class="file-preview"
        >
          <img :src="file.url" class="img-thumbnail" />
          <button
            @click="removeFile(index)"
            class="btn btn-danger btn-sm"
          >
            <i class="fas fa-times"></i>
          </button>
          <p>{{ file.name }}</p>
        </div>
        <button
          class="btn btn-primary mt-3 w-100"
          @click="processFiles"
          :disabled="isLoading"
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
      files: [],
      isLoading: false,
    };
  },
  methods: {
    handleFileSelect(event) {
      const selectedFiles = Array.from(event.target.files);
      selectedFiles.forEach((file) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.files.push({
            name: file.name,
            url: e.target.result,
            file,
          });
        };
        reader.readAsDataURL(file);
      });
    },
    removeFile(index) {
      this.files.splice(index, 1);
    },
    async processFiles() {
      this.isLoading = true;
      try {
        const formData = new FormData();
        this.files.forEach((file) => {
          formData.append("files", file.file)
        });

        const objectName = this.$store.state.global.formData.objectName;
        formData.append("objectName", objectName);

        await axios.post(`${process.env.VITE_API_URL}/upload`, formData);
        console.log("Uploaded files");
        this.$router.push("/model-view");
      } catch (error) {
        console.error("Error uploading files:", error);
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.file-preview {
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
  background-color: transparent;
  border: none;
}
</style>
