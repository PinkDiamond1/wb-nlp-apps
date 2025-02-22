<template>
  <div>
    <h3>{{ page_title }}</h3>
    <br />

    <p>
      Topics are not covered evenly over time, across regions, by document type,
      and by organization represented in our corpus. Select a source, a topic
      and a (LDA) model, and two or more partitions to compare the evolution of
      the topic coverage over time. The resulting chart can be embedded, its
      code downloaded, and the underlying data are available in our document
      meta-database.
    </p>

    <hr />

    <b-container fluid>
      <MLModelSelect @modelSelected="onModelSelect" :model_name="model_name" />

      <br />

      <b-row v-show="model_run_info_id !== null">
        <b-col :md="show_topic_words ? 9 : 12">
          <b-row
            v-if="
              lda_model_id != '' &&
              topic_share_active &&
              current_lda_model_topics_options
            "
          >
            <b-col cols="10">
              <b-form-group>
                <!-- <v-select
                  class="topic-chooser"
                  id="topic_id"
                  placeholder="Select topic"
                  v-model="selected_topic"
                  label="text"
                  :options="current_lda_model_topics_options"
                >
                  <template #selected-option="{ text }">
                    <div style="width: 100%">
                      <span id="topic-selected">
                        {{ text }}
                      </span>
                    </div>
                  </template></v-select
                > -->
                <!--
                <b-form-select
                  id="topic_id"
                  v-model="topic_id"
                  :options="current_lda_model_topics_options"
                >
                  <template #first>
                    <b-form-select-option value="" disabled
                      >-- Please select a topic --</b-form-select-option
                    >
                  </template></b-form-select
                > -->

                <!-- <b-form-input
                  v-model="topic_id"
                  list="my-list-id"
                ></b-form-input>
                <datalist id="my-list-id" style="width: 100%">
                  <option>Select topic...</option>
                  <option
                    v-for="cto in current_lda_model_topics_options"
                    :key="cto.topic_id"
                  >
                    {{ cto.text }}
                  </option>
                </datalist> -->

                <model-select
                  :options="current_lda_model_topics_options"
                  v-model="topic_id"
                  placeholder="Select topic"
                >
                </model-select>
              </b-form-group>
            </b-col>

            <b-col cols="2">
              <div>
                <b-dropdown
                  split
                  v-on:click="readyForSubmit ? findTopicShare() : null"
                  :split-variant="
                    readyForSubmit ? 'success' : 'outline-primary'
                  "
                  variant="primary"
                  :text="readyForSubmit ? 'Plot' : 'Select'"
                >
                  <b-dropdown-form class="checkbox">
                    <b-form-group label="Admin Region">
                      <b-form-checkbox-group
                        v-model="topic_share_selected_adm_regions"
                        :options="adm_regions"
                        stacked
                      ></b-form-checkbox-group>
                    </b-form-group>
                    <b-form-group label="Document Type">
                      <b-form-checkbox-group
                        v-model="topic_share_selected_doc_types"
                        :options="doc_types"
                        stacked
                      ></b-form-checkbox-group>
                    </b-form-group>
                    <!-- <b-form-group label="Lending Instrument">
                      <b-form-checkbox-group
                        v-model="topic_share_selected_lending_instruments"
                        :options="lending_instruments"
                        stacked
                      ></b-form-checkbox-group>
                    </b-form-group> -->
                  </b-dropdown-form>
                  <b-dropdown-item-button disabled
                    ><span> </span
                  ></b-dropdown-item-button>
                </b-dropdown>
              </div>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <div v-show="!topic_shares && !topic_share_plot_ready">
                Start exploring topic shares by selecting the topic of interest
                and select the data partitions to compare.
              </div>

              <div :class="blurContent ? 'blur' : ''">
                <Plotly
                  v-show="topic_share_plot_ready"
                  :data="plot_data"
                  :layout="plot_layout"
                  :display-mode-bar="false"
                ></Plotly>
              </div>
              <div
                v-show="
                  (!topic_share_plot_ready && topic_shares) ||
                  topic_share_searching
                "
              >
                <b-skeleton-img></b-skeleton-img>
              </div>
            </b-col>
          </b-row>
        </b-col>
        <b-col
          :md="show_topic_words ? 3 : 0"
          v-show="show_topic_words"
          class="border-left"
        >
          <h4>Topic words</h4>

          <div
            v-show="
              (!topic_share_plot_ready && topic_shares) || topic_share_searching
            "
          >
            <b-skeleton-table
              animation="wave"
              :rows="10"
              :columns="1"
              :table-props="{ bordered: true, striped: true }"
            ></b-skeleton-table>
          </div>
          <div
            v-show="topic_share_plot_ready"
            :class="blurContent ? 'blur' : ''"
          >
            <b-list-group flush>
              <b-list-group-item
                v-for="topic_word in topic_words"
                :key="'topic_word-' + topic_word.word"
              >
                {{ topic_word.word }}
              </b-list-group-item>
            </b-list-group>
          </div></b-col
        >
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { Plotly } from "vue-plotly";
import $ from "jquery";
import MLModelSelect from "../common/MLModelSelect";
import { ModelSelect } from "vue-search-select";

export default {
  name: "TopicProfiles",
  components: {
    Plotly,
    MLModelSelect,
    ModelSelect,
  },
  props: {
    page_title: String,
    show_topic_words: Boolean,
  },
  data: function () {
    return {
      errors: [],
      api_url: "/api",
      nlp_api_url: null,
      model_topics: [],
      related_words: [],
      current_lda_model_topics: [],
      current_lda_model_topics_options: [],
      raw_text: "poverty",
      loading: true,
      model_name: "lda",
      model_run_info_id: null,

      corpus_id: "WB",
      lda_model_id: "ALL_50",

      topic_share_active: true,

      prev_topic_id: -1,
      topic_id: null,
      selected_topic: 0,
      topic_share_selected_adm_regions: [],
      topic_share_selected_doc_types: [],
      topic_share_selected_lending_instruments: [],
      topic_share_plot_ready: false,
      topic_share_searching: false,

      topic_shares: null,
      topic_words: null,

      // Doc types specific to WB document. Must be changed when updating the metadata.
      adm_regions: [
        "Africa",
        "East Asia and Pacific",
        "Europe and Central Asia",
        "Latin America & Caribbean",
        "Middle East and North Africa",
        "Rest Of The World",
        "South Asia",
        "The world Region",
      ],
      doc_types: [
        "Board Documents",
        "Country Focus",
        "Economic & Sector Work",
        "Project Documents",
        "Publications & Research",
      ],
      lending_instruments: ["Development Policy Lending"],

      // Plotly data and layout
      plot_data: [
        {
          x: [1, 2, 3, 4],
          y: [10, 15, 13, 17],
          type: "scatter",
        },
      ],
      plot_layout: {
        title: "My graph",
      },
    };
  },
  computed: {
    // topic_id() {
    //   return this.selected_topic.topic_id;
    // },
    searchParams() {
      const params = new URLSearchParams();
      params.append("model_id", this.model_run_info_id);
      params.append("topn_words", 10);
      return params;
    },
    readyForSubmit: function () {
      return (
        this.topic_share_selected_adm_regions.length +
          this.topic_share_selected_doc_types.length +
          this.topic_share_selected_lending_instruments.length >
        0
      );
    },
    topicChanged: function () {
      // return this.prev_topic_id != this.selected_topic.topic_id;
      return this.prev_topic_id != this.topic_id;
    },
    blurContent: function () {
      return this.topicChanged || !this.topic_share_plot_ready;
    },
  },
  mounted() {
    // window.vm = this;
    this.setModel();
  },
  methods: {
    onModelSelect: function (result) {
      this.model_run_info_id = result.model_run_info_id;
      this.nlp_api_url = result.url;
      this.getModelTopics();
    },
    formatTopicText: function (topic) {
      return (
        "Topic " +
        topic.topic_id +
        ": " +
        topic.topic_words
          .slice(0, 8)
          .map(function (x) {
            return x.word;
          })
          .join(", ")
      );
    },
    getModelTopics: function () {
      this.$http
        .get(this.nlp_api_url + "/get_model_topic_words", {
          params: this.searchParams,
        })
        .then((response) => {
          // this.model_topics = response.data;
          this.current_lda_model_topics = response.data;
          this.current_lda_model_topics_options = this.lodash.map(
            this.current_lda_model_topics,
            (topic) => {
              return {
                text: this.formatTopicText(topic),
                value: topic.topic_id,
              };
            }
          );
          this.topic_words = this.current_lda_model_topics[this.topic_id];
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
        })
        .finally(() => (this.loading = false));
    },
    setModel: function (_model_id, model_name) {
      _model_id = "ALL_50";
      model_name = "lda";
      let vm = this;
      if (model_name == "word2vec") {
        vm.word2vec_model_id = _model_id;
      } else if (model_name == "lda") {
        // Assume that
        vm.lda_model_id = _model_id;

        // let options = {
        //   corpus_id: this.corpus_id,
        //   model_id: this.lda_model_id,
        //   topn_words: 10,
        // };

        let options = {
          // model_id: "6694f3a38bc16dee91be5ccf4a64b6d8",
          model_id: this.model_run_info_id,
          topn_words: 10,
        };

        this.$http
          // .get(this.api_url + "/get_lda_model_topics" + "?" + $.param(options))
          .get(
            this.nlp_api_url + "/get_model_topic_words" + "?" + $.param(options)
          )
          .then((response) => {
            this.current_lda_model_topics = response.data;
            this.current_lda_model_topics_options = this.lodash.map(
              this.current_lda_model_topics,
              (topic) => {
                return {
                  text: this.formatTopicText(topic),
                  value: topic.topic_id,
                };
              }
            );
            this.topic_words = this.current_lda_model_topics[this.topic_id];
          })
          .catch((error) => {
            console.log(error);
            this.errored = true;
          })
          .finally(() => (this.loading = false));
      } else {
        return;
      }
    },
    findTopicShare: function () {
      this.prev_topic_id = this.topic_id;
      this.topic_share_searching = true;
      this.topic_share_plot_ready = false;

      // let options = {
      //   corpus_id: this.corpus_id,
      //   model_id: this.lda_model_id,
      //   topic_id: this.topic_id,
      //   year_start: 1960,
      //   adm_regions: this.topic_share_selected_adm_regions,
      //   major_doc_types: this.topic_share_selected_doc_types,
      //   lending_instruments: this.topic_share_selected_lending_instruments,
      // };

      let options = {
        corpus_id: this.corpus_id,
        // model_id: "6694f3a38bc16dee91be5ccf4a64b6d8",
        model_id: this.model_run_info_id,
        topic_id: this.topic_id,
        year_start: 1960,
        adm_regions: this.topic_share_selected_adm_regions,
        major_doc_types: this.topic_share_selected_doc_types,
      };

      this.$http
        // .post(this.api_url + "/lda_compare_partition_topic_share", options)
        .post(this.nlp_api_url + "/get_partition_topic_share", options)
        .then((response) => {
          let data = response.data;

          if ("topic_shares" in data) {
            this.topic_shares = data.topic_shares;
          }
          if ("topic_words" in data) {
            this.topic_words = data.topic_words;
          }
          console.log(data);
        })
        .catch((error) => {
          console.log(error);
          this.errors.push(error);
          this.errored = true;
        })
        .finally(() => {
          this.topic_share_searching = false;
          this.plotStack(this.topic_shares);
        });
    },
    plotStack: function (topic_shares) {
      this.topic_share_plot_ready = false;

      let keys = Object.keys(topic_shares);
      let traces = [];

      let ph = 250.0;
      let ps = 50.0;

      let height = ph * keys.length + ps * (keys.length - 1);
      let div_dt = ps / height;
      let panel_dt = ph / height;

      let layout = {
        title: "Topic share per document group",
        xaxis: { domain: [0, 1], title: "Year" },
        height: height,
        autosize: true,
      };

      let ix = 1;
      let yd_start = 0;
      let yd_end = yd_start + panel_dt;
      let max_y = 0;
      let part_name = "";
      let y, y_max, tr;

      for (part_name in topic_shares) {
        y = topic_shares[part_name].map(function (x) {
          return x.topic_share;
        });
        y_max = Math.max.apply(null, y);

        if (y_max > max_y) {
          max_y = y_max;
        }

        tr = {
          x: topic_shares[part_name].map(function (x) {
            return x.year;
          }),
          y: y,
          name: part_name,
          type: "bar",
        };
        if (ix > 1) {
          tr.xaxis = "x";
          tr.yaxis = "y" + ix;
        }

        traces.push(tr);
        ix += 1;
      }

      for (ix = 1; ix <= keys.length; ix++) {
        if (ix > 1) {
          layout["yaxis" + ix] = {
            domain: [yd_start, yd_end],
            range: [0, max_y],
          };
        } else {
          layout.yaxis = { domain: [yd_start, yd_end], range: [0, max_y] };
        }

        yd_start = yd_end + div_dt;
        yd_end = yd_start + panel_dt;
      }

      layout.legend = { orientation: "h", x: 0, y: 1 };

      console.log(traces);
      console.log(layout);

      this.plot_data = traces;
      this.plot_layout = layout;
      this.topic_share_plot_ready = true;
      this.prev_topic_id = this.topic_id;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#topic-selected {
  width: 42vw;
  text-overflow: ellipsis;
  overflow: hidden;
  display: block;
  white-space: nowrap;
}
/* #topic-selected > div {
  position: absolute;
} */

/* .vs--single .vs__selected {
  text-overflow: ellipsis;
  color: #394066;
} */
.blur {
  filter: blur(1px);
  opacity: 0.4;
}

.checkbox /deep/ .b-dropdown-form {
  max-height: 400px;
  font-size: 75%;
  overflow-y: auto;
}
</style>
