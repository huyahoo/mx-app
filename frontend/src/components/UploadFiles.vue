<template>
  <div class="container mt-md-5">
    <div class="card mx-auto">
      <div class="card-body">
        <h5 class="card-title text-center">Upload Files</h5>
        <input
          id="file"
          type="file"
          multiple
          @change="handleFileSelect"
          class="form-control"
          accept="image/*"
          style="display: none"
        />
        <label for="file" class="image-label custom-file-upload" v-show="!isLoading">
          Choose File
          <i class="bi bi-cloud-upload-fill ms-2" style="font-size: 16px"></i>
        </label>
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
          <p class="image-label">{{ file.name }}</p>
        </div>
        <button
          class="btn btn-primary mt-3 w-100"
          @click="processFiles"
          :disabled="!isValid || isLoading"
        >
          <i
            v-if="isLoading"
            class="fas fa-spinner fa-spin"
          ></i>
          <span v-else>
            <i class="fas fa-cogs me-1"></i>
            Process
          </span>
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
  computed: {
    isValid() {
      return this.files.length > 0;
    },
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
.custom-file-upload {
  width: 100%;
  height: 120px;
  padding: 10px;
  border: 2px dashed #79a4e4;
  border-radius: 10px;
  display: inline-block;
  cursor: pointer;
  justify-content: center;
  align-items: center;
  display: flex;
}
.card {
  max-height: 756px;
  max-width: 310px;
  overflow: hidden;
}
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
  font-size: 16px;
}
.image-label {
  color: gray;
  font-size: 14px;
  font-weight: 500;
}
</style>
