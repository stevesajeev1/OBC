<template>
  <div :class="$style.card">
    <div :class="$style.card2" />
    <div :class="$style.bimBob">{{ handle }}</div>
    <div :class="$style.prevInternships">
      <div :class="$style.internedAt">Interned at: </div>
      <img :src="companyIcon" :class="$style.phIcon" alt="company" />
    </div>
    <div :class="$style.name">
      <div :class="$style.bimBob2">{{ fullName }}</div>
    </div>
    <img :src="backIcon" :class="$style.backArrowIcon" alt="back" @click="emitClose" />
    <img :src="profileImage" :class="$style.cardChild" alt="profile" />

    <!-- Social / Contact Section -->
    <div :class="$style.emailParent">
      <div :class="$style.email">
        <img :src="emailIcon" :class="$style.miemailIcon" alt="email" />
        <div :class="$style.bimbobgmailcom">bimbob@gmail.com</div>
      </div>
      <div :class="$style.instagram">
        <img :src="instagramIcon" :class="$style.miemailIcon" alt="instagram" />
        <div :class="$style.bimbobgmailcom">bimbob_insta</div>
      </div>
      <div :class="$style.instagram">
        <img :src="linkedinIcon" :class="$style.mdilinkedinIcon" alt="linkedin" />
        <div :class="$style.bimbobgmailcom">Bim Bob</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

const props = withDefaults(defineProps<{
  username?: string;
  fullName?: string;
  profileImageUrl?: string;
  companyIconUrl?: string;
}>(), {
  username: 'bim_bob'
});

const emit = defineEmits<{ (e: 'close'): void }>();
const emitClose = () => emit('close');

const handle = computed(() => props.username || 'bim_bob');
const fullName = computed(() =>
  props.fullName || handle.value.split('_').map((s) => s.charAt(0).toUpperCase() + s.slice(1)).join(' ')
);

// Image assets (allow override via props)
const profileImage = computed(
  () => props.profileImageUrl || 'https://media.discordapp.net/attachments/778002970112557116/1443639418362789928/bimbob.png?ex=6929cd7a&is=69287bfa&hm=f28318ffc79a8e4d6c0a364b07a3fef787cd450974fbcee180e634d054abeaff&=&format=webp&quality=lossless'
);
const companyIcon = computed(
  () => props.companyIconUrl || 'https://media.discordapp.net/attachments/778002970112557116/1443639943519014912/googlelogo.png?ex=6929cdf8&is=69287c78&hm=d4336bb1cfdaa688b3a04d0a806ed5f512e13ee321e4a1d583d5e6f5960e7a35&=&format=webp&quality=lossless'
);
// Simple inline SVG left arrow as data URL
const backIcon = ref(
  'data:image/svg+xml;utf8,' +
    encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>')
);

// Simple inline icons
const emailIcon = ref(
  'data:image/svg+xml;utf8,' +
    encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16v16H4z"/><path d="M22 6l-10 7L2 6"/></svg>')
);
const instagramIcon = ref(
  'data:image/svg+xml;utf8,' +
    encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.5" y2="6.5"/></svg>')
);
const linkedinIcon = ref(
  'data:image/svg+xml;utf8,' +
    encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="45" height="45" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-14h4v2a4 4 0 0 1 4-2z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>')
);
</script>

<style module>
.card {
  width: 899px;
  max-width: 100%;
  height: 684px;
  position: relative;
  text-align: left;
  font-size: 24px;
  color: #fff;
  font-family: 'Inria Sans';
}
.card2 {
  position: absolute;
  top: 0px;
  left: 0px;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 50px;
  background: linear-gradient(180deg, rgba(30, 144, 255, 0.75) 95.67%, #d4862d);
  border: 1px solid #d4862d;
  box-sizing: border-box;
  width: 100%;
  height: 684px;
}
.bimBob {
  position: absolute;
  top: 22px;
  left: 747px;
}
.prevInternships {
  position: absolute;
  top: 507px;
  left: 574px;
  display: flex;
  align-items: flex-end;
  gap: 17px;
  font-size: 36px;
}
.internedAt {
  position: relative;
}
.phIcon {
  height: 40px;
  width: 40px;
  position: relative;
  border-radius: 50%;
  object-fit: cover;
}
.name {
  position: absolute;
  top: 365px;
  left: 327px;
  width: 244px;
  height: 77px;
  font-size: 64px;
  font-family: 'Irish Grover';
}
.bimBob2 {
  position: absolute;
  top: 0px;
  left: 0px;
  text-shadow: 1px 0 0 #000, 0 1px 0 #000, -1px 0 0 #000, 0 -1px 0 #000;
}
.backArrowIcon {
  position: absolute;
  top: 31px;
  left: 43px;
  width: 40px;
  height: 40px;
  object-fit: contain;
  cursor: pointer;
}
.cardChild {
  position: absolute;
  top: 50px;
  left: 301px;
  border-radius: 50%;
  width: 300px;
  height: 300px;
  object-fit: cover;
}

/* Social / Contact Section */
.emailParent {
  position: absolute;
  top: 474px;
  right: 551px;
  bottom: 65px;
  left: 80px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
  text-align: left;
  font-size: 24px;
  color: #fff;
  font-family: 'Inria Sans';
}
.email {
  align-self: stretch;
  display: flex;
  align-items: center;
  gap: 17px;
}
.miemailIcon {
  width: 40px;
  position: relative;
  max-height: 100%;
}
.bimbobgmailcom {
  position: relative;
}
.instagram {
  display: flex;
  align-items: center;
  gap: 17px;
}
.mdilinkedinIcon {
  width: 45px;
  position: relative;
  max-height: 100%;
}
</style>
