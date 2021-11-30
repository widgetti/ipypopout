<template>
  <span>
    <v-btn
        v-if="!isInPopupMode() && kernel_id"
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
  methods: {
    getBaseUrl() {
      const labConfigData = document.getElementById('jupyter-config-data');
      if (labConfigData) {
        /* lab */
        return JSON.parse(labConfigData.textContent).baseUrl;
      }
      const bodyBaseUrl = document.body.dataset.baseUrl
      return bodyBaseUrl.endsWith('/voila/') ? bodyBaseUrl.slice(0, - 'voila/'.length) : bodyBaseUrl;
    },
    getUrl() {
      const baseUrl = this.getBaseUrl();
      const result = `${location.protocol}//${location.host}${baseUrl}${this.popoutPageUrl}` +
          `?kernelid=${this.kernel_id}&modelid=${this.target_model_id}&baseurl=${baseUrl}`

      return result;
    },
    openWindow() {
      window.open(this.getUrl(), this.target_model_id, 'resizable=yes');
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
