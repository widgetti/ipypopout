<template>
  <span>
    <v-btn
        v-if="!isInPopupMode() && kernel_id && getBaseUrl()"
        @click="openWindow"
        @contextmenu.prevent="openTab"
        icon
        :disabled="!echo_available"
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
  mounted() {
    this.is_displayed = true;
    if (this.open_window_on_display) {
      this.open_window_on_display = false;
      this.openWindow();
    }
    if (this.open_tab_on_display) {
      this.open_tab_on_display = false;
      this.openTab();
    }
  },
  methods: {
    getBaseUrl() {
      const labConfigData = document.getElementById('jupyter-config-data');
      if (labConfigData) {
        /* lab and Voila */
        return JSON.parse(labConfigData.textContent).baseUrl;
      }
      return document.body.dataset.baseUrl
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
      const params = new URLSearchParams(window.location.search);
      return params.get('modelid') == this.target_model_id;
    },
    jupyter_open_window() {
      this.openWindow();
    },
    jupyter_open_tab() {
      this.openTab();
    }
  },
  computed: {
    popoutPageUrl() {
       if (window.solara && (solara.rootPath !== undefined)) {
        return solara.rootPath;
      }
      return 'voila/templates/ipypopout/static/popout.html'
    }
  }
}
</script>
