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
  data() {
    return {solaraFound: false}
  },
  created() {
    const baseUrl = this.getBaseUrl();
    if (!baseUrl) {
      this.solaraDetectionPromise = Promise.resolve();
      console.info('BaseUrl not found, hiding popout button.');
    } else {
      const solaraReadyZUrl = `${baseUrl}solara/readyz`;
      this.solaraDetectionPromise = fetch(solaraReadyZUrl)
        .then(response => {
          if (response.ok) {
            console.error('Solara found, using Solara popout page.');
            this.solaraFound = true;
          }
        })
    }
  },
  mounted() {
    this.is_displayed = true;
    this.solaraDetectionPromise.then(() => {
      if (this.open_window_on_display) {
        this.open_window_on_display = false;
        this.openWindow();
      }
      if (this.open_tab_on_display) {
        this.open_tab_on_display = false;
        this.openTab();
      }
    });
  },
  methods: {
    getBaseUrl() {
      if(window.solara) { 
        // if on solara >=1.40, the jupyter base url is different from the solara one
        return window.solara.rootPath + "/";
      }
      const labConfigData = document.getElementById('jupyter-config-data');
      if (labConfigData) {
        /* lab, Voila, and Solara */
        return JSON.parse(labConfigData.textContent).baseUrl;
      }
      return document.body.dataset.baseUrl
    },
    getUrl() {
      const isDark = this.$root.$vuetify.theme.isDark
      const baseUrl = this.getBaseUrl();
      const host = document.body.dataset.voilaHost || `${location.protocol}//${location.host}`
      const result = `${host}${baseUrl}${this.popoutPageUrl}` +
          `?kernelid=${this.kernel_id}&modelid=${this.target_model_id}&baseurl=${baseUrl}` + (isDark ? '&dark=true' : '');

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
        return ""
      }
      if(this.use_backend == "solara" || (this.use_backend == "auto" && this.solaraFound)) {
        return 'solara';
      } else {
        return 'voila/templates/ipypopout/static/popout.html'
      }
    }
  }
}
</script>
