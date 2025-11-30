<template>
  <div class="edit-profile-modal-overlay" @click="closeModal">
    <div class="edit-profile-modal" @click.stop>
      <div class="modal-header">
        <h2>Edit Profile</h2>
        <button class="close-button" @click="closeModal">X</button>
      </div>

      <div class="modal-content">
        <div class="profile-image-section">
          <div class="image-preview">
            <img :src="form.image_url" alt="Profile Preview" class="profile-preview" />
          </div>
          <input type="file" accept="image/*" @change="handleImageUpload" class="file-input" id="profile-image-input" />
          <label for="profile-image-input" class="upload-button"> Change Profile Picture </label>
        </div>

        <div class="form-group">
          <label for="name">Full Name</label>
          <input type="text" id="name" v-model="form.name" placeholder="Enter your full name" class="form-input" />
        </div>

        <div class="form-group">
          <label for="email">Email Address</label>
          <input type="email" id="email" v-model="form.email" placeholder="Enter your email" class="form-input" />
        </div>

        <div class="modal-actions">
          <button class="cancel-button" @click="closeModal">Cancel</button>
          <button class="save-button" @click="saveProfile">Save Changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import { getProfile } from '@/api/profile';

  const router = useRouter();

  const form = ref({
    name: '',
    email: '',
    image_url: ''
  });

  // Load current profile data
  onMounted(async () => {
    const currentProfile = getProfile();
    if (currentProfile) {
      form.value = {
        name: currentProfile.name || '',
        email: currentProfile.email || '',
        image_url:
          currentProfile.image_url ||
          'https://cdn.vectorstock.com/i/500p/29/52/faceless-male-avatar-in-hoodie-vector-56412952.jpg'
      };
    }
  });

  const closeModal = () => {
    router.back();
  };

  const handleImageUpload = (event: Event) => {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const file = input.files[0];
      const reader = new FileReader();

      reader.onload = e => {
        if (e.target?.result) {
          form.value.image_url = e.target.result as string;
        }
      };

      reader.readAsDataURL(file);
    }
  };

  const saveProfile = () => {
    console.log('Saving profile:', form.value);
    closeModal();
  };
</script>

<style scoped>
  .edit-profile-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(90, 124, 175, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2000;
  }

  .edit-profile-modal {
    background: #7a9ccf;
    border-radius: 15px;
    width: 90%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    border: 3px solid #000;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border-bottom: 2px solid #000;
    background: #5a7caf;
    border-radius: 12px 12px 0 0;
    color: white;
    font-family: 'Irish Grover', cursive;
  }

  .modal-header h2 {
    margin: 0;
    color: #d4862d;
    text-shadow:
      -1px -1px 0 #000,
      1px -1px 0 #000,
      -1px 1px 0 #000,
      1px 1px 0 #000;
  }

  .close-button {
    background: none;
    border: 2px solid #d4862d;
    border-radius: 50%;
    font-size: 1.5rem;
    cursor: pointer;
    color: #d4862d;
    font-weight: bold;
    transition: all 0.3s ease;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Irish Grover', cursive;
  }

  .close-button:hover {
    background: #d4862d;
    color: white;
  }

  .modal-content {
    padding: 20px;
  }

  .profile-image-section {
    text-align: center;
    margin-bottom: 20px;
  }

  .image-preview {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 3px solid #000;
    overflow: hidden;
    margin: 0 auto 15px;
    background: #f0f0f0;
  }

  .profile-preview {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .file-input {
    display: none;
  }

  .upload-button {
    display: inline-block;
    background: #d4862d;
    color: white;
    padding: 8px 16px;
    border-radius: 5px;
    cursor: pointer;
    border: 2px solid #000;
    font-family: 'Irish Grover', cursive;
    transition: opacity 0.3s ease;
  }

  .upload-button:hover {
    opacity: 0.8;
  }

  .form-group {
    margin-bottom: 20px;
  }

  .form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: white;
    font-family: 'Irish Grover', cursive;
    text-shadow:
      -1px -1px 0 #000,
      1px -1px 0 #000,
      -1px 1px 0 #000,
      1px 1px 0 #000;
  }

  .form-input {
    width: 100%;
    padding: 12px;
    border: 2px solid #000;
    border-radius: 5px;
    font-size: 1rem;
    background: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }

  .form-input:focus {
    outline: none;
    border-color: #d4862d;
  }

  .modal-actions {
    display: flex;
    gap: 15px;
    justify-content: flex-end;
    margin-top: 30px;
  }

  .cancel-button,
  .save-button {
    padding: 12px 24px;
    border: 2px solid #000;
    border-radius: 5px;
    cursor: pointer;
    font-family: 'Irish Grover', cursive;
    font-size: 1rem;
    transition: all 0.3s ease;
  }

  .cancel-button {
    background: #000;
    color: #d4862d;
  }

  .cancel-button:hover {
    opacity: 0.8;
  }

  .save-button {
    background: #d4862d;
    color: white;
  }

  .save-button:hover {
    opacity: 0.8;
    transform: translateY(-2px);
  }
</style>
