<template>
  <div>
    <b-row align-v="center">
      <b-col>
        <p class="lead" style="font-size: 3rem">
          {{ titleHeader }}
        </p></b-col
      ><b-col>
        <div style="overflow: hidden; margin-right: 50px">
          <b-button
            style="float: right"
            @click="setResetEvent()"
            :variant="resetButtonVariant"
            :disabled="disableReset"
            >Reset</b-button
          >

          <b-button
            style="float: right; margin: 0 10px 0 10px"
            @click="setPauseEvent()"
            :variant="pauseButtonVariant"
            :disabled="disablePause"
            >{{ paused ? "Resume" : "Pause" }}</b-button
          >
        </div></b-col
      >
    </b-row>
    <h5>{{ partition_type }}</h5>
    <div
      class="vue-world-map"
      @mouseover="should_pause = true"
      @mouseleave="should_pause = false"
    >
      <WBMap
        @hoverCountry="onHoverCountry"
        @hoverLeaveCountry="onHoverLeaveCountry"
      />
      <div
        v-if="legend.name"
        class="vue-map-legend"
        :style="'left:' + position.left + 'px; top: ' + position.top + 'px'"
      >
        <div class="vue-map-legend-header">
          <span>{{ legend.name }}</span>
        </div>
        <div class="vue-map-legend-content">
          <span>{{ getDisplayValue(legend.code) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import chroma from "chroma-js";
import WBMap from "../wb/WBMap";
import {
  getDynamicMapCss,
  getBaseCss,
  getCombinedCssString,
} from "../../js/dynamic-map-css";
let legend = {
  data: null,
  code: null,
  name: null,
};
let position = {
  left: 0,
  top: 0,
};
export default {
  name: "AnimatedMapChartWB",
  components: { WBMap },
  watch: {
    countryData() {
      this.renderMapCSS();
    },
    timeseriesCountryData() {
      this.clearQueue();
      this.startAnimation();
    },
    loaded() {
      if (this.loaded) {
        this.$emit("ready", this.loaded);
      }
    },
  },
  computed: {
    disableReset() {
      return !this.stopped && !this.paused;
    },
    disablePause() {
      return this.stopped;
    },
    resetButtonVariant() {
      var variant = "outline-secondary";

      if (this.stopped || this.paused) {
        variant = "primary";
      }
      return variant;
    },
    pauseButtonVariant() {
      var variant = "primary";

      if (this.paused) {
        variant = "success";
      }
      if (this.stopped) {
        variant = "outline-secondary";
      }
      return variant;
    },
    pauseAnimation() {
      return (
        (this.pause_loop || this.should_pause || this.paused) &&
        !this.break_loop
      );
    },
    titleHeader() {
      var title = "Resetting...";
      if (!this.break_loop) {
        title = this.current_year
          ? this.current_year.split("-")[0]
          : "Loading...";
      }

      return title;
    },
  },
  props: {
    partition_type: {
      type: String,
      default: "",
    },
    pause_loop: {
      type: Boolean,
      default: false,
    },
    nodeId: {
      type: String,
      default: "mapChartStyleNode",
    },
    lowColor: {
      type: String,
      default: "#fde2e2",
    },
    highColor: {
      type: String,
      default: "#d83737",
    },
    chromaScaleOn: {
      type: Boolean,
      default: true,
    },
    timeseriesCountryData: {
      type: Object,
      required: true,
    },
    defaultCountryFillColor: {
      type: String,
      default: "#dadada",
    },
    countryStrokeColor: {
      type: String,
      default: "#909090",
    },
    countryStrokeWidth: {
      type: String,
      default: "0.5px",
    },
    xxxMaskStrokeWidth: {
      type: String,
      default: "0.75px",
    },
    xxxStrokeDashArray: {
      type: String,
      default: "1 1",
    },
    legendHeaderBackgroundColor: {
      type: String,
      default: "white",
    },
    legendContentBackgroundColor: {
      type: String,
      default: "#dadbda8f",
    },
    legendFontColorHeader: {
      type: String,
      default: "black",
    },
    legendFontColorContent: {
      type: String,
      default: "black",
    },
    legendBorderColor: {
      type: String,
      default: "gray",
    },
    legendBorderRadius: {
      type: Number,
      default: 5,
    },
    legendBoxShadow: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      processedCountryData: null,
      countryData: null,
      current_year: null,
      legend: legend,
      position: position,
      node: this.getOrCreateNode(),
      chromaScale: chroma.scale([this.$props.lowColor, this.$props.highColor]),
      should_pause: false,
      loaded: false,

      stopped: false,
      paused: false,
      break_loop: false,

      queue: [],
    };
  },
  methods: {
    setPauseEvent() {
      this.paused = !this.paused;
    },
    setResetEvent() {
      this.stopped = false;
      this.paused = false;
      this.clearQueue();
      this.startAnimation();
      this.break_loop = false;
    },
    processNormalizeCountryData() {
      if (this.countryData === null || this.countryData === undefined) {
        return;
      } else if (Object.keys(this.countryData).length === 0) {
        return;
      }
      var totalCount = Object.values(this.countryData).reduce((a, b) => a + b);

      var processedCountryData = JSON.parse(JSON.stringify(this.countryData));
      // var processedCountryData = this.countryData;
      Object.keys(processedCountryData).forEach(
        (k) => (processedCountryData[k] = processedCountryData[k] / totalCount)
      );

      var cnVal = processedCountryData.CN || 0;
      var inVal = processedCountryData.IN || 0;
      var sdudVal = processedCountryData.SD || 0;
      var ssudVal = processedCountryData.SS || 0;

      // Set values for disputed areas
      if (cnVal + inVal > 0) {
        processedCountryData.XXX_arunachal_pradesh = (cnVal + inVal) / 2;
        processedCountryData.XXX_demchok = (cnVal + inVal) / 2;
        processedCountryData.XXX_aksai_chin = (cnVal + inVal) / 2;
      }

      if (sdudVal + ssudVal > 0) {
        processedCountryData.XXX_abyei = (sdudVal + ssudVal) / 2;
      }

      processedCountryData.XXX_western_sahara = "No data";

      this.processedCountryData = JSON.parse(
        JSON.stringify(processedCountryData)
      );

      if (!this.loaded) {
        this.loaded = true;
      }
    },
    getDisplayValue(code) {
      if (!this.processedCountryData) {
        return "No data";
      }
      var value = this.processedCountryData[code];
      if (value === "No data") {
        return value;
      }

      if (isNaN(value)) {
        return 0;
      }

      return (100 * value).toFixed(2) + "% | Count: " + this.countryData[code];
    },
    getOrCreateNode() {
      var node = document.getElementById(this.nodeId);
      if (!node) {
        node = document.createElement("style");
        node.id = this.nodeId;
      }
      return node;
    },
    onHoverCountry(country) {
      if (
        country.code.startsWith("XXX_") &&
        country.name !== "Western Sahara"
      ) {
        return;
      }
      this.legend = country;
      this.position = country.position;
      this.$emit("hoverCountry", country);
      // this.should_pause = true;
    },
    onHoverLeaveCountry(country) {
      this.legend = {
        data: null,
        code: null,
        name: null,
      };
      // this.should_pause = false;
      this.$emit("hoverLeaveCountry", country);
    },
    renderMapCSS() {
      this.processNormalizeCountryData();
      if (!this.$data.processedCountryData) {
        return;
      }

      this.$data.node.remove();
      this.$data.node = this.getOrCreateNode();
      document.body.appendChild(this.$data.node);
      // console.log("TESTESTEST");

      const baseCss = getBaseCss(this.$props);
      const dynamicMapCss = getDynamicMapCss(
        // this.$props.countryData,
        this.$data.processedCountryData,
        this.chromaScale,
        this.$props.highColor,
        this.$props.chromaScaleOn
      );

      this.$data.node.innerHTML = getCombinedCssString(baseCss, dynamicMapCss);
    },
    startAnimation() {
      this.break_loop = false;
      const years = Object.keys(this.timeseriesCountryData).sort();
      let vm = this;
      // console.log(years);
      const num_years = years.length;

      (function myLoop(i) {
        vm.queue.push(
          setTimeout(function () {
            if (vm.pauseAnimation) {
              console.log("Looping");
              // (function pauseBuffer(pause) {
              //   setTimeout(() => {
              //     console.log("Buffer...");
              //     if (pause) pauseBuffer(vm.pause_loop || vm.should_pause);
              //     return;
              //   }, 1000);
              // })(vm.pause_loop || vm.should_pause);
            } else if (vm.break_loop) {
              // console.log("Loop terminated");
              return;
            } else {
              var ix = num_years - i;

              vm.countryData = vm.timeseriesCountryData[years[ix]];
              vm.current_year = years[ix];
              i = i - 1;
              if (vm.current_year === years[years.length - 1]) {
                vm.stopped = true;
              }
            }
            const setTimeoutID = vm.queue.shift();
            clearTimeout(setTimeoutID);
            if (i) myLoop(i); //  decrement i and call myLoop again if i > 0
          }, 1000)
        );
      })(num_years);
    },
    clearQueue() {
      this.break_loop = true;
      this.queue.forEach((panel) => clearTimeout(panel));
      this.queue = [];
    },
  },
  mounted() {
    // document.body.appendChild(this.$data.node);
    // this.startAnimation();

    // this.renderMapCSS();
    // window.mapVM = this;
    this.$emit("mounted", true);
  },
  destroyed() {
    this.clearQueue();
    this.$emit("destroyed", true);
  },
};
</script>

<style scoped>
.vue-world-map,
#map-svg {
  height: 100%;
}
.vue-world-map {
  position: relative;
}
.vue-map-legend {
  width: 185px;
  background: #fff;
  overflow: auto;
  border: 1px solid;
  position: absolute;
}
.vue-map-legend-header {
  padding: 10px 15px;
}
.vue-map-legend-content {
  padding: 10px 15px;
  background: #dadbda8f;
  border-top: 1px solid #acacad;
}
</style>