<template>
  <span>
    <v-btn
        v-if="!isInPopupMode() && kernel_id && getBaseUrl()"
        @click="openWindow"
        @contextmenu.prevent="openTab"
        icon
    >
      <v-icon>mdi-application-export</v-icon>
    </v-btn>
  </span>
</template>
<script>
module.exports = {
  created() {
    if (!this.getBaseUrl()) {
      console.info('BaseUrl not found, hiding popout button.');
    }
  },
  methods: {
    getBaseUrl() {
      const labConfigData = document.getElementById('jupyter-config-data');
      if (labConfigData) {
        /* lab */
        return JSON.parse(labConfigData.textContent).baseUrl;
      }
      const bodyBaseUrl = document.body.dataset.baseUrl
      if (!bodyBaseUrl) {
        return;
      }
      return bodyBaseUrl.endsWith('/voila/') ? bodyBaseUrl.slice(0, - 'voila/'.length) : bodyBaseUrl;
    },
    getUrl() {
      const baseUrl = this.getBaseUrl();
      const host = document.body.dataset.voilaHost || `${location.protocol}//${location.host}`
      const result = `${host}${baseUrl}${this.popoutPageUrl}` +
          `?kernelid=${this.kernel_id}&modelid=${this.target_model_id}&baseurl=${baseUrl}`

      return result;
    },
    openWindow() {
      window.open(this.getUrl(), this.window_name, this.window_features);
    },
    openTab() {
      window.open(this.getUrl(), '_blank');
    },
    isInPopupMode() {
      return window.location.pathname.includes(this.popoutPageUrl);
    }
  },
  computed: {
    popoutPageUrl() {
      return 'voila/templates/ipypopout/static/popout.html'
    }
  }
}
</script>
