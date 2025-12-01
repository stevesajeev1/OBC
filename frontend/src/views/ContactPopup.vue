<template>
  <div :class="$style.card">
    <div :class="$style.card2" />
    <div :class="$style.bimBob">{{ handle }}</div>
    <div :class="$style.prevInternships">
      <div :class="$style.internedAt">Interned&nbsp;at:</div>
      <div :class="$style.companyIconsRow">
        <div v-for="(icon, idx) in companyIcons" :key="idx" :class="$style.companyItem">
          <img :src="icon" :class="$style.phIcon" alt="company" @error="onCompanyLogoError" />
          <span :class="$style.companyName">{{ companyNames[idx] || '' }}</span>
        </div>
      </div>
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
        <div :class="$style.bimbobgmailcom">{{ props.email }}</div>
      </div>
      <div :class="$style.instagram">
        <img :src="instagramIcon" :class="$style.miemailIcon" alt="instagram" />
        <div :class="$style.bimbobgmailcom">{{ props.instagram }}</div>
      </div>
      <div :class="$style.instagram">
        <img :src="linkedinIcon" :class="$style.mdilinkedinIcon" alt="linkedin" />
        <a :href="linkedinHref" :class="$style.bimbobgmailcom" target="_blank" rel="noopener noreferrer">LinkedIn</a>
      </div>
      <!-- Roles List -->
      <div :class="$style.rolesList">
        <div :class="$style.internedAt">Roles:</div>
        <ul :class="$style.rolesUl">
          <li v-for="(role, idx) in roles" :key="idx">{{ role }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { computed, ref } from 'vue';

  const props = withDefaults(
    defineProps<{
      username?: string;
      fullName?: string;
      profileImageUrl?: string;
      companyIconUrl?: string;
      email?: string;
      instagram?: string;
      linkedin?: string;
      roles?: string[];
      companyIcons?: string[];
      companyNames?: string[];
    }>(),
    {
      username: 'bim_bob',
      email: 'bimbob@gmail.com',
      instagram: 'bimbob_insta',
      linkedin: 'Bim Bob',
      roles: () => [],
      companyIcons: () => [],
      companyNames: () => []
    }
  );

  const emit = defineEmits<{ (e: 'close'): void }>();
  const emitClose = () => emit('close');

  const handle = computed(() => props.username || 'bim_bob');
  const fullName = computed(
    () =>
      props.fullName ||
      handle.value
        .split('_')
        .map(s => s.charAt(0).toUpperCase() + s.slice(1))
        .join(' ')
  );

  // Image assets (allow override via props)
  const profileImage = computed(() => props.profileImageUrl || '/assets/default_pfp.jpg');
  const companyIcons = computed(() =>
    props.companyIcons && props.companyIcons.length
      ? props.companyIcons
      : props.companyIconUrl
        ? [props.companyIconUrl]
        : []
  );
  const roles = computed(() => props.roles || []);
  const companyNames = computed(() => props.companyNames || []);
  // Simple inline SVG left arrow as data URL
  const backIcon = ref(
    'data:image/svg+xml;utf8,' +
      encodeURIComponent(
        '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>'
      )
  );

  // Simple inline icons
  const emailIcon = ref(
    'data:image/svg+xml;utf8,' +
      encodeURIComponent(
        '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16v16H4z"/><path d="M22 6l-10 7L2 6"/></svg>'
      )
  );
  const instagramIcon = ref(
    'data:image/svg+xml;utf8,' +
      encodeURIComponent(
        '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.5" y2="6.5"/></svg>'
      )
  );
  const linkedinIcon = ref(
    'data:image/svg+xml;utf8,' +
      encodeURIComponent(
        '<svg xmlns="http://www.w3.org/2000/svg" width="45" height="45" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-14h4v2a4 4 0 0 1 4-2z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>'
      )
  );

  const linkedinHref = computed(() => {
    const v = props.linkedin || '';
    if (!v) return 'https://www.linkedin.com';
    if (/^https?:\/\//i.test(v)) return v;
    if (v.startsWith('www.linkedin.com')) return `https://${v}`;
    return `https://www.linkedin.com/in/${v}`;
  });

  function onCompanyLogoError(e: Event) {
    const img = e.target as HTMLImageElement;
    if (img && !img.src.endsWith('/assets/default_company.jpeg')) {
      img.src = '/assets/default_company.jpeg';
    }
  }
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
    font-family: 'Irish Grover';
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
    left: 540px;
    display: flex;
    flex-wrap: nowrap;
    align-items: flex-end;
    gap: 12px;
    font-size: 36px;
  }
  .internedAt {
    position: relative;
    white-space: nowrap;
    word-break: keep-all;
  }
  .companyIconsRow {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  .companyItem {
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .companyName {
    font-family: 'Irish Grover';
    font-size: 24px;
    line-height: 1.1;
    white-space: nowrap;
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
    left: 50%;
    transform: translateX(-50%);
    width: auto;
    max-width: 600px;
    height: 77px;
    font-size: 64px;
    font-family: 'Irish Grover';
    text-align: center;
  }
  .bimBob2 {
    position: relative;
    top: 0px;
    text-shadow:
      1px 0 0 #000,
      0 1px 0 #000,
      -1px 0 0 #000,
      0 -1px 0 #000;
    white-space: nowrap;
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
    font-family: 'Irish Grover';
    /* Ensure children (roles list) can scroll within this area */
    overflow: hidden;
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
  .rolesList {
    margin-top: 8px;
    color: #fff;
    font-family: 'Irish Grover';
    /* Take remaining space and enable vertical scrolling for long lists */
    flex: 1 1 auto;
    min-height: 0;
    overflow-y: auto;
    padding-right: 8px; /* space for scrollbar */
  }
  .rolesUl {
    margin: 6px 0 0 0;
    padding: 0 0 0 18px;
    list-style: disc;
  }
</style>
