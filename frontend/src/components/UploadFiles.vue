<template>
  <div class="container mt-3 mt-md-5">
    <div class="card mx-auto" :class="cardClass">
      <div class="card-body text-center">
        <h5 class="card-title">Upload Files</h5>
        <input type="file" ref="fileInput" multiple @change="handleFileSelect" class="form-control">
        <div v-for="(file, index) in selectedFiles" :key="index" class="preview-container">
          <img v-if="file.type.startsWith('image/')" :src="file.preview" alt="preview" class="img-thumbnail">
          <p>{{ file.name }}</p>
          <!-- <button class="btn btn-danger btn-sm remove-btn" @click="removeFile(index)">x</button> -->
          <button type="button" class="btn-close remove-btn" aria-label="Close"></button>
        </div>
        <button class="btn btn-primary mt-3 w-100" @click="uploadFiles">Process</button>
        <!-- <button type="button" class="btn-close" aria-label="Close" @click="getPresignUrl">Get Image</button> -->

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFiles: []
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
    handleFileSelect(event) {
      const files = Array.from(event.target.files);
      files.forEach(file => {
        const reader = new FileReader();
        reader.onload = (e) => {
          file.preview = e.target.result;
          this.selectedFiles.push(file);
        };
        reader.readAsDataURL(file);
      });
    },
    removeFile(index) {
      this.selectedFiles.splice(index, 1);
    },
    async uploadFiles() {
      const formData = new FormData();
      this.selectedFiles.forEach(file => {
        formData.append('files', file);
      });

      try {
        const response = await axios.post('http://localhost:5000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('Files uploaded successfully:', response.status);
        this.$router.push('/model-view');
      } catch (error) {
        console.error('Error uploading files:', error);
      }
    },
    async getPresignUrl() {
      // const file = this.selectedFiles[0];
      const file = 'IMG_5991.JPG';
      const response = await axios.get(`http://localhost:5000/get-image?filename=${file}`);
      console.log('Presign URL:', response.data);
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
  /* max-width: 100%; Ensure the card does not exceed screen width */
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
  /* background-color: red; */
  border: none;
  color: white;
  font-size: 1rem;
  line-height: 1rem;
  padding: 0.2rem;
  border-radius: 50%;
}
@media (min-width: 768px) {
  .card {
    max-width: 400px;
  }
}
</style>
