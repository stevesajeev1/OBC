<template>
  <div class="edit-profile-modal-overlay" @click="closeModal">
    <div class="edit-profile-modal" @click.stop>
      <div class="modal-header">
        <h2>Edit Profile</h2>
        <button class="close-button" @click="closeModal">X</button>
      </div>

      <div class="modal-content">
        <!-- Profile Image Section -->
        <div class="profile-image-section">
          <div class="image-preview">
            <img :src="profileImageUrl" alt="Profile Preview" class="profile-preview" />
          </div>
          <input
            type="file"
            accept="image/*"
            @change="handleImageUpload"
            class="file-input"
            id="profile-image-input"
            :disabled="imageUploading"
          />
          <label for="profile-image-input" class="upload-button" :class="{ disabled: imageUploading }">
            {{ imageUploading ? 'Uploading...' : 'Change Profile Picture' }}
          </label>
          <button
            v-if="form.image_url"
            class="remove-image-button"
            @click="removeProfileImage"
            :disabled="imageUploading"
          >
            Remove Image
          </button>
        </div>

        <!-- Full Name -->
        <div class="form-group">
          <label for="full_name">Full Name *</label>
          <input
            type="text"
            id="full_name"
            v-model="form.full_name"
            placeholder="Enter your full name"
            class="form-input"
          />
          <span class="error-message" v-if="!form.full_name?.trim()">Full name is required</span>
        </div>

        <!-- Major -->
        <div class="form-group">
          <label for="major">Major</label>
          <input type="text" id="major" v-model="form.major" placeholder="e.g., Computer Science" class="form-input" />
        </div>

        <!-- Graduation Year -->
        <div class="form-group">
          <label for="grad_year">Graduation Year</label>
          <input
            type="number"
            id="grad_year"
            v-model="form.grad_year"
            placeholder="e.g., 2025"
            class="form-input"
            min="2000"
            :max="new Date().getFullYear() + 6"
          />
        </div>

        <!-- LinkedIn URL -->
        <div class="form-group">
          <label for="linkedin_url">LinkedIn URL</label>
          <input
            type="url"
            id="linkedin_url"
            v-model="form.linkedin_url"
            placeholder="https://linkedin.com/in/yourprofile"
            class="form-input"
          />
        </div>

        <!-- Bio -->
        <div class="form-group">
          <label for="bio">Bio</label>
          <textarea
            id="bio"
            v-model="form.bio"
            placeholder="Tell us about yourself..."
            class="form-input textarea"
            rows="4"
          ></textarea>
        </div>

        <!-- Public Profile Checkbox -->
        <div class="form-group checkbox-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="form.public" class="checkbox" />
            Make profile public
          </label>
          <small class="hint">When checked, other users can see your profile</small>
        </div>

        <!-- Modal Actions -->
        <div class="modal-actions">
          <button class="cancel-button" @click="closeModal" :disabled="loading || imageUploading">Cancel</button>
          <button class="save-button" @click="saveProfile" :disabled="!canSave || loading || imageUploading">
            {{ loading ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted, computed } from 'vue';
  import { useRouter } from 'vue-router';
  import { getProfile, updateProfile, uploadProfileImage, deleteProfileImage, type ProfileUpdate } from '@/api/profile';

  const router = useRouter();

  const defaultAvatar = 'https://cdn.vectorstock.com/i/500p/29/52/faceless-male-avatar-in-hoodie-vector-56412952.jpg';
  const loading = ref(false);
  const imageUploading = ref(false);

  const form = ref<ProfileUpdate>({
    full_name: '',
    major: null,
    grad_year: null,
    linkedin_url: null,
    bio: null,
    image_url: null,
    public: true
  });

  const originalProfile = ref<ProfileUpdate | null>(null);

  const profileImageUrl = computed(() => form.value.image_url || defaultAvatar);

  const canSave = computed(() => !!form.value?.full_name?.trim().length);

  const hasChanges = computed(() => {
    if (!originalProfile.value) return false;
    return JSON.stringify(form.value) !== JSON.stringify(originalProfile.value);
  });

  // Load current profile
  onMounted(async () => {
    try {
      loading.value = true;
      const currentProfile = await getProfile();
      if (currentProfile) {
        originalProfile.value = { ...currentProfile };
        form.value = {
          full_name: currentProfile.full_name || '',
          major: currentProfile.major,
          grad_year: currentProfile.grad_year,
          linkedin_url: currentProfile.linkedin_url,
          bio: currentProfile.bio,
          image_url: currentProfile.image_url,
          public: currentProfile.public !== false
        };
      }
    } catch (error) {
      console.error('Failed to load profile:', error);
      alert('Failed to load profile data.');
    } finally {
      loading.value = false;
    }
  });

  const closeModal = () => {
    if (hasChanges.value && !confirm('You have unsaved changes. Are you sure you want to leave?')) return;
    router.back();
  };

  // Upload new profile image
  const handleImageUpload = async (event: Event) => {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const file = input.files[0];

      if (file.size > 4.5 * 1024 * 1024) {
        alert('Image size should be less than 4.5MB');
        input.value = '';
        return;
      }

      if (!file.type.startsWith('image/')) {
        alert('Please select a valid image file');
        input.value = '';
        return;
      }

      try {
        imageUploading.value = true;
        await uploadProfileImage(file);

        const updatedProfile = await getProfile();
        if (updatedProfile?.image_url) form.value.image_url = updatedProfile.image_url;

        alert('Profile image updated successfully!');
        input.value = '';
      } catch (error) {
        console.error('Failed to upload image:', error);
        alert('Failed to upload profile image. Please try again.');
      } finally {
        imageUploading.value = false;
      }
    }
  };

  // Remove profile image
  const removeProfileImage = async () => {
    if (!confirm('Are you sure you want to remove your profile image?')) return;

    try {
      imageUploading.value = true;
      await deleteProfileImage();
      form.value.image_url = null;
      alert('Profile image removed successfully!');
    } catch (error) {
      console.error('Failed to remove image:', error);
      alert('Failed to remove profile image. Please try again.');
    } finally {
      imageUploading.value = false;
    }
  };

  // Save profile changes
  const saveProfile = async () => {
    if (!canSave.value) {
      alert('Please provide a full name to save your profile.');
      return;
    }

    if (!hasChanges.value) {
      alert('No changes detected.');
      return;
    }

    try {
      loading.value = true;
      await updateProfile({ ...form.value });
      alert('Profile updated successfully!');
      closeModal();
      setTimeout(() => window.location.reload(), 500);
    } catch (error) {
      console.error('Failed to update profile:', error);
      alert('Failed to update profile. Please try again.');
    } finally {
      loading.value = false;
    }
  };
</script>

<style scoped>
  /* Keep all your existing styles, including profile image, buttons, modal, etc. */
</style>

<style scoped>
  /* Your existing styles remain the same, just add this new button style */
  .remove-image-button {
    display: block;
    background: #ff6b6b;
    color: white;
    padding: 8px 16px;
    border-radius: 5px;
    cursor: pointer;
    border: 2px solid #000;
    font-family: 'Irish Grover', cursive;
    transition: opacity 0.3s ease;
    margin: 10px auto 0;
  }

  .remove-image-button:hover:not(:disabled) {
    opacity: 0.8;
  }

  .remove-image-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .upload-button.disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  /* Your existing styles below... */
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

  .upload-button:hover:not(.disabled) {
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

  .form-input:read-only {
    background-color: #f5f5f5;
    cursor: not-allowed;
  }

  .textarea {
    resize: vertical;
    min-height: 80px;
  }

  .checkbox-group {
    display: flex;
    flex-direction: column;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
  }

  .checkbox {
    width: 18px;
    height: 18px;
    cursor: pointer;
  }

  .hint {
    color: #e0e0e0;
    font-size: 0.85rem;
    margin-top: 5px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }

  .error-message {
    color: #ff6b6b;
    font-size: 0.85rem;
    margin-top: 5px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    text-shadow: none;
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

  .cancel-button:hover:not(:disabled) {
    opacity: 0.8;
  }

  .save-button {
    background: #d4862d;
    color: white;
  }

  .save-button:hover:not(:disabled) {
    opacity: 0.8;
    transform: translateY(-2px);
  }

  .save-button:disabled,
  .cancel-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
</style>
