<template>
  <div class="container mt-3 mt-md-5">
    <div class="card mx-auto" :class="cardClass">
      <div class="card-body text-center">
        <h5 class="card-title">Model Views</h5>
        <div class="form-group mb-3 label__input">
          <label for="objects" class="form-label">Objects</label>
          <select v-model="selectedObject" @change="loadModel" class="form-select">
            <option v-for="object in objects" :key="object" :value="object">{{ object }}</option>
          </select>
        </div>
        <div class="model-viewer-container">
          <model-viewer id="glb" :src="selectedObject" ar ar-modes="webxr scene-viewer quick-look" camera-controls tone-mapping="neutral" poster="poster.webp" shadow-intensity="1" style="width: 100%; height: 310px;">
            <div class="progress-bar hide" slot="progress-bar">
                <div class="update-bar"></div>
            </div>
          </model-viewer>
        </div>
        <button class="btn btn-primary mt-3 w-100" @click="downloadModel" :disabled="!selectedObject">
          <i v-if="isLoading" class="fas fa-spinner fa-spin"></i>
          <span v-else>
            <i class="bi bi-cloud-arrow-down-fill me-1"></i>
            Download
          </span>
        </button>
        <button class="btn btn-secondary mt-2 w-100" @click="useThreeJS" :disabled="!selectedObject">
          <i v-if="isLoadingThreeJS" class="fas fa-spinner fa-spin"></i>
          <span v-else>
            Enter
            <i class="bi bi-badge-vr-fill me-1"></i>
          </span>
        </button>
        <div v-if="isLoadingModel" class="loading-overlay">
          <div class="spinner"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      objects: [],
      selectedObject: '',
      modelSrc: 'wolvic_3d_model.glb',
      isLoading: false,
      isLoadingModel: false,
      isLoadingThreeJS: false
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
  async created() {
    await this.getModels();
  },
  methods: {
    async getModels() {
      this.isLoadingModel = true;
      try {
        const res = await axios.get(`${process.env.VITE_API_URL}/get-models`);
        this.objects = res.data;
        if (this.objects.length > 0) {
          this.objects = res.data.map((model) => model.split('/')[1]);
          this.selectedObject = this.objects[0];
          this.loadModel();
        }
      } catch (error) {
        console.error('Error getting models:', error);
      } finally {
        this.isLoadingModel = false;
      }
    },
    async loadModel() {
      if (this.selectedObject) {
        this.isLoadingModel = true;
        const file = `output/${this.selectedObject}`;
        const res = await axios.get(`${process.env.VITE_API_URL}/get-image?filename=${file}`);
        const modelViewerElement = document.getElementById('glb');
        modelViewerElement.src = res.data;

        modelViewerElement.addEventListener('load', () => {
            this.isLoadingModel = false;
        }, { once: true });
      }
    },
    async downloadModel() {
      this.isLoading = true;
      try {
        const link = document.createElement('a');
        link.href = this.modelSrc;
        link.download = this.selectedObject;
        link.click();
      } catch (error) {
        console.error('Error downloading model:', error);
      } finally {
        this.isLoading = false;
      }
    },
    useThreeJS() {
      this.isLoadingThreeJS = true;
      this.isLoadingThreeJS = false;
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
.model-viewer-container {
  margin-top: 10px;
  background-color: #f3f3f3;
  border-radius: 10px;
  overflow: hidden;
}
.spinner {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #000;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
</style>
