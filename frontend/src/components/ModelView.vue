<template>
  <div class="container mt-3 mt-md-5">
    <div class="card mx-auto" :class="cardClass">
      <div class="card-body text-center">
        <h5 class="card-title">Model Views</h5>
        <div class="form-group">
          <label for="objects">Objects</label>
          <select v-model="selectedObject" @change="loadModel" class="form-control">
            <option v-for="object in objects" :key="object" :value="object">{{ object }}</option>
          </select>
        </div>
        <div class="model-viewer-container">
          <!-- <model-viewer 
            v-if="modelSrc" 
            :src="modelSrc" 
            alt="3D Model" 
            auto-rotate 
            camera-controls 
            style="width: 100%; height: 300px;">
          </model-viewer> -->

          <!-- <model-viewer style="width: 100%; height: 300px;" id = "glb" crossorigin="anonymous" camera-controls ></model-viewer> -->

          <model-viewer src="wolvic_3d_model.glb" ar ar-modes="webxr scene-viewer quick-look" camera-controls tone-mapping="neutral" poster="poster.webp" shadow-intensity="1">
            <div class="progress-bar hide" slot="progress-bar">
                <div class="update-bar"></div>
            </div>
            <!-- <button slot="ar-button" id="ar-button">
                View in your space
            </button> -->
            <!-- <div id="ar-prompt">
                <img src="https://modelviewer.dev/shared-assets/icons/hand.png">
            </div> -->
          </model-viewer>

          <!-- <model-viewer camera-controls touch-action="pan-y" alt="A 3D model of a sphere" src="./2CylinderEngine.glb">
          </model-viewer> -->
        </div>
        <button class="btn btn-primary mt-3 w-100" @click="downloadModel">Download</button>
        <button class="btn btn-secondary mt-2 w-100" @click="useThreeJS">ThreeJS</button>
      </div>
    </div>
  </div>
</template>

<!-- <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script> -->

<script>
import axios from 'axios';

export default {
  data() {
    return {
      objects: ["a", "b"],
      selectedObject: 'a',
      modelSrc: '/Users/huyphung/Repositories/personal/mx-app/wolvic_3d_model.glb'
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
    // await this.loadObjects();
  },
  methods: {
    async loadObjects() {
      try {
        const response = await axios.get('http://localhost:5000/s3-objects');
        this.objects = response.data.objects;
        if (this.objects.length > 0) {
          this.selectedObject = this.objects[0];
          this.loadModel();
        }
      } catch (error) {
        console.error('Error loading objects:', error);
      }
    },
    async loadModel() {
      if (this.selectedObject) {
        // this.modelSrc = `https://your-s3-bucket-url/${this.selectedObject}`;
        // this.modelSrc = '/Users/huyphung/Repositories/personal/mx-app/wolvic_3d_model.glb';
        const file = 'wolvic_3d_model.glb';
        const response = await axios.get(`http://localhost:5000/get-image?filename=${file}`);
        console.log(response.data)
        document.getElementById('glb').src = response.data;
        // this.modelSrc = response.data;
      }
    },
    downloadModel() {
      const link = document.createElement('a');
      link.href = this.modelSrc;
      link.download = this.selectedObject;
      link.click();
    },
    useThreeJS() {
      // Handle navigation to ThreeJS implementation screen
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
  font-size: 1.5rem;
  font-weight: bold;
}
.model-viewer-container {
  margin-top: 10px;
  background-color: #f3f3f3;
  border-radius: 10px;
  overflow: hidden;
}
</style>
