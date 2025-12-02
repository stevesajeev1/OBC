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
            v-if="currentImageUrl !== defaultPfp"
            class="remove-image-button"
            @click="removeProfileImage"
            :disabled="imageUploading"
          >
            Remove Image
          </button>
        </div>

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

        <div class="form-group">
          <label for="major">Major</label>
          <input type="text" id="major" v-model="form.major" placeholder="e.g., Computer Science" class="form-input" />
        </div>

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

        <div class="form-group internships-section">
          <div class="section-header">
            <label>Previous Internships</label>
            <button
              type="button"
              class="add-internship-button"
              @click="addInternship"
              :disabled="loading || imageUploading"
            >
              + Add Internship
            </button>
          </div>

          <div class="internships-list">
            <div v-for="(internship, index) in form.prev_internships" :key="index" class="internship-item">
              <div class="internship-header">
                <h4>Internship #{{ index + 1 }}</h4>
                <button type="button" class="remove-internship-button" @click="removeInternship(index)">Remove</button>
              </div>

              <div class="internship-fields">
                <div class="form-group">
                  <label :for="`company-${index}`">Company *</label>
                  <input
                    type="text"
                    :id="`company-${index}`"
                    v-model="internship.company"
                    placeholder="e.g., Google"
                    class="form-input"
                    :class="{ error: !internship.company?.trim() }"
                  />
                  <span class="error-message" v-if="!internship.company?.trim()">Company is required</span>
                </div>

                <div class="form-group">
                  <label :for="`role-${index}`">Role *</label>
                  <input
                    type="text"
                    :id="`role-${index}`"
                    v-model="internship.role"
                    placeholder="e.g., Software Engineering Intern"
                    class="form-input"
                    :class="{ error: !internship.role?.trim() }"
                  />
                  <span class="error-message" v-if="!internship.role?.trim()">Role is required</span>
                </div>

                <div class="form-group">
                  <label :for="`time_period-${index}`">Time Period *</label>
                  <div class="time-period-inputs">
                    <input
                      type="text"
                      :id="`time_period-start-${index}`"
                      v-model="internship.time_period[0]"
                      placeholder="Start (e.g., Summer 2023)"
                      class="form-input time-period-input"
                      :class="{ error: !internship.time_period[0]?.trim() }"
                    />
                    <span class="time-period-separator">to</span>
                    <input
                      type="text"
                      :id="`time_period-end-${index}`"
                      v-model="internship.time_period[1]"
                      placeholder="End (e.g., Fall 2023)"
                      class="form-input time-period-input"
                      :class="{ error: !internship.time_period[1]?.trim() }"
                    />
                  </div>
                  <span
                    class="error-message"
                    v-if="!internship.time_period[0]?.trim() || !internship.time_period[1]?.trim()"
                  >
                    Time period is required
                  </span>
                </div>
              </div>
            </div>
          </div>

          <small class="hint">Add your previous internship experiences to showcase your background</small>
        </div>

        <div class="form-group checkbox-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="form.public" class="checkbox" />
            Make profile public
          </label>
          <small class="hint">When checked, other users can see your profile</small>
        </div>

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
  import { ref, onMounted, computed, defineEmits } from 'vue';
  import { useRouter } from 'vue-router';
  import { getProfile, updateProfile, uploadProfileImage, deleteProfileImage, type ProfileUpdate } from '@/api/profile';
  import defaultPfp from '@/assets/default_pfp.jpg';

  const router = useRouter();
  const emit = defineEmits<{
    (e: 'profile-updated', updatedProfile: { full_name: string; image_url: string }): void;
  }>();

  const loading = ref(false);
  const imageUploading = ref(false);

  const currentImageUrl = ref<string>(defaultPfp);

  const form = ref<ProfileUpdate>({
    full_name: '',
    major: null,
    grad_year: null,
    linkedin_url: null,
    bio: null,
    prev_internships: [],
    public: false
  });

  const originalProfile = ref<ProfileUpdate | null>(null);

  const profileImageUrl = computed(() => currentImageUrl.value);

  const canSave = computed(() => {
    if (!form.value?.full_name?.trim().length) return false;

    if (form.value.prev_internships) {
      for (const internship of form.value.prev_internships) {
        if (
          !internship.company?.trim() ||
          !internship.role?.trim() ||
          !internship.time_period[0]?.trim() ||
          !internship.time_period[1]?.trim()
        ) {
          return false;
        }
      }
    }

    return true;
  });

  const hasChanges = computed(() => {
    if (!originalProfile.value) return false;
    return JSON.stringify({ ...form.value }) !== JSON.stringify({ ...originalProfile.value });
  });

  onMounted(async () => {
    try {
      loading.value = true;
      const currentProfile = await getProfile();
      if (currentProfile) {
        currentImageUrl.value = currentProfile.image_url || defaultPfp;

        originalProfile.value = {
          full_name: currentProfile.full_name,
          major: currentProfile.major,
          grad_year: currentProfile.grad_year,
          linkedin_url: currentProfile.linkedin_url,
          bio: currentProfile.bio,
          prev_internships: currentProfile.prev_internships ? [...currentProfile.prev_internships] : [],
          public: currentProfile.public
        };

        form.value = {
          ...originalProfile.value,
          prev_internships: currentProfile.prev_internships ? [...currentProfile.prev_internships] : []
        };

        if (form.value.prev_internships) {
          form.value.prev_internships = form.value.prev_internships.map(internship => ({
            ...internship,
            time_period: internship.time_period?.length === 2 ? [...internship.time_period] : ['', '']
          }));
        }
      }
    } catch (error) {
      console.error('Failed to load profile:', error);
      alert('Failed to load profile data.');
    } finally {
      loading.value = false;
    }
  });

  const addInternship = () => {
    if (!form.value.prev_internships) {
      form.value.prev_internships = [];
    }

    form.value.prev_internships.push({
      company: '',
      role: '',
      time_period: ['', '']
    });
  };

  const removeInternship = (index: number) => {
    if (form.value.prev_internships) {
      form.value.prev_internships.splice(index, 1);
    }
  };

  const closeModal = () => {
    if (hasChanges.value && !confirm('You have unsaved changes. Are you sure you want to leave?')) return;
    router.back();
  };

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
        currentImageUrl.value = updatedProfile?.image_url || defaultPfp;

        emit('profile-updated', {
          full_name: form.value.full_name || '',
          image_url: currentImageUrl.value
        });

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

  const removeProfileImage = async () => {
    if (!confirm('Are you sure you want to remove your profile image?')) return;

    try {
      imageUploading.value = true;
      await deleteProfileImage();
      currentImageUrl.value = defaultPfp;

      emit('profile-updated', {
        full_name: form.value.full_name || '',
        image_url: currentImageUrl.value
      });

      alert('Profile image removed successfully!');
    } catch (error) {
      console.error('Failed to remove image:', error);
      alert('Failed to remove profile image. Please try again.');
    } finally {
      imageUploading.value = false;
    }
  };

  const saveProfile = async () => {
    if (!canSave.value) {
      alert('Please provide all required fields (marked with *) to save your profile.');
      return;
    }

    if (!hasChanges.value) {
      alert('No changes detected.');
      return;
    }

    try {
      loading.value = true;
      const updatedProfile = await updateProfile({ ...form.value });

      emit('profile-updated', {
        full_name: updatedProfile.full_name || '',
        image_url: currentImageUrl.value
      });

      alert('Profile updated successfully!');
      originalProfile.value = { ...form.value };
      closeModal();
    } catch (error) {
      console.error('Failed to update profile:', error);
      alert('Failed to update profile. Please try again.');
    } finally {
      loading.value = false;
    }
  };
</script>

<style scoped>
  * {
    font-family: 'Irish Grover', cursive;
  }

  .remove-image-button {
    display: block;
    background: #ff6b6b;
    color: white;
    padding: 8px 16px;
    border-radius: 5px;
    cursor: pointer;
    border: 2px solid #000;
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

  .internships-section {
    background: rgba(90, 124, 175, 0.2);
    padding: 15px;
    border-radius: 8px;
    border: 2px solid #000;
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
  }

  .section-header label {
    margin-bottom: 0;
  }

  .add-internship-button {
    background: #d4862d;
    color: white;
    padding: 8px 16px;
    border-radius: 5px;
    cursor: pointer;
    border: 2px solid #000;
    transition: all 0.3s ease;
    font-size: 0.9rem;
  }

  .add-internship-button:hover {
    opacity: 0.8;
    transform: translateY(-2px);
  }

  .internships-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-bottom: 10px;
  }

  .internship-item {
    background: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 5px;
    border: 2px solid #000;
  }

  .internship-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid #000;
  }

  .internship-header h4 {
    margin: 0;
    color: white;
    text-shadow:
      -1px -1px 0 #000,
      1px -1px 0 #000,
      -1px 1px 0 #000,
      1px 1px 0 #000;
  }

  .remove-internship-button {
    background: #ff6b6b;
    color: white;
    padding: 6px 12px;
    border-radius: 5px;
    cursor: pointer;
    border: 2px solid #000;
    transition: opacity 0.3s ease;
    font-size: 0.8rem;
  }

  .remove-internship-button:hover:not(:disabled) {
    opacity: 0.8;
  }

  .remove-internship-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .internship-fields {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  .time-period-inputs {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .time-period-input {
    flex: 1;
  }

  .time-period-separator {
    color: white;
    font-weight: bold;
    text-shadow:
      -1px -1px 0 #000,
      1px -1px 0 #000,
      -1px 1px 0 #000,
      1px 1px 0 #000;
  }

  .form-input.error {
    border-color: #ff6b6b;
  }

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
    font-family: 'Irish Grover', cursive;
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
    font-family: 'Irish Grover', cursive;
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
  }

  .error-message {
    color: #ff6b6b;
    font-size: 0.85rem;
    margin-top: 5px;
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
  .add-internship-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  .form-input::placeholder {
    font-family: 'Irish Grover', cursive;
    color: #999;
  }
</style>
