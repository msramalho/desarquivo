<template>
  <div class="flex-grow-1 d-flex">
    <network-canvas v-on:ready="canvasReady" v-on:expandEntity="expandEntity" />
    <filter-form
      v-on:selectEntity="selectEntity"
      v-on:runLayout="runLayout"
      v-on:updateSelectedLabels="updateSelectedLabels"
      v-on:updateLimit="updateLimit"
      v-on:invertSelection="invertSelection"
      v-on:expandSelected="expandSelected"
      v-on:deleteSelected="deleteSelected"
      v-on:updateFilterRange="updateFilterRange"
      v-on:connectSelectedSingle="connectSelectedSingle"
      v-on:connectSelected="connectSelected"
      v-on:downloadPng="downloadPng"
      v-on:downloadJson="downloadJson"
      v-on:intersectSelected="intersectSelected"
      :countSelectedNodes="countSelectedNodes"
      :countSelectedEdges="countSelectedEdges"
      :loadingCard="loading"
    />
    <news-drawer
      :show="(countSelectedNodes==1&&countSelectedEdges==0) || (countSelectedNodes==0&&countSelectedEdges==1)"
      :displayText="displayText"
      :selectedEdge="selectedEdge"
      :selectedNode="selectedNode"
      v-on:addEntity="selectEntity"
    />
  </div>
</template>

<script>
import FilterForm from "~/components/FilterForm.vue";
import NetworkCanvas from "~/components/NetworkCanvas.vue";
import NewsDrawer from "~/components/NewsDrawer.vue";
import { saveAs } from "file-saver";

export default {
  data() {
    return {
      limit: 50,
      selectedLabels: ["PER", "ORG", "LOC", "MISC"],
      countSelectedNodes: 0,
      countSelectedEdges: 0,
      range: { min: 0, max: 100 },
      minWeight: 0,
      maxWeight: 100,
      loading: false,
      selectedEdge: undefined,
      selectedNode: undefined,
      doubleClicked: false,
      displayText: ""
    };
  },
  methods: {
    selectEntity(entity) {
      this.addNode(this.entityToNode(entity));
    },
    canvasReady({ cy, context }) {
      this.cy = cy;
      this.context = context;
      this.setListeners();
    },
    setListeners() {
      this.cy.on("doubleClick", "node", e => this.expandEntity(e.target));
      this.cy.on("select", "node", this.updateCountSelectedNodes);
      this.cy.on("unselect", "node", this.updateCountSelectedNodes);
      this.cy.on("select", "edge", this.updateCountSelectedEdges);
      this.cy.on("unselect", "edge", this.updateCountSelectedEdges);
    },
    updateCountSelectedNodes(e) {
      this.cy.$("edge.selectedEdge").removeClass("selectedEdge");
      setTimeout(() => {
        if (this.doubleClicked) return;
        let selNodes = this.cy.$("node:selected");
        this.countSelectedNodes = selNodes.size();
        this.countSelectedEdges = this.cy.$("edge:selected").size();
        if (
          this.countSelectedNodes == 1 &&
          this.cy.$("edge:selected").size() == 0
        ) {
          selNodes[0].connectedEdges().addClass("selectedEdge");
          this.selectedNode = selNodes[0].data();
          this.displayText = this.selectedNode.text;
          this.selecteEdge = undefined;
        }
        this.updateContextMenu();
      }, 350);
    },
    updateCountSelectedEdges(e) {
      // this.cy.$("edge.selectedEdge").removeClass("selectedEdge");
      let selEdges = this.cy.$("edge:selected");
      this.countSelectedEdges = selEdges.size();
      this.countSelectedNodes = this.cy.$("node:selected").size();
      if (this.countSelectedEdges == 1 && this.countSelectedNodes == 0) {
        this.selectedEdge = selEdges[0].data();
        this.displayText = `${this.$t("canvas.link")} <b>${
          this.cy.$id(this.selectedEdge.source).data().text
        }</b> - <b>${this.cy.$id(this.selectedEdge.target).data().text}</b>`;
        this.selectedNode = undefined;
      }
      this.updateContextMenu();
    },
    updateContextMenu() {
      if (this.countSelectedNodes <= 1) {
        this.context.showMenuItem("expand");
        this.context.showMenuItem("revertExpand");
        this.context.showMenuItem("selectConnections");
      } else {
        this.context.hideMenuItem("expand");
        this.context.hideMenuItem("revertExpand");
        this.context.hideMenuItem("selectConnections");
      }
    },
    updateLimit(newLimit) {
      this.limit = { 0: 30, 1: 50, 2: 150, 3: 300, 4: "inf" }[newLimit];
    },
    updateSelectedLabels(labels) {
      this.selectedLabels = labels;
      this.filterEntities();
    },
    updateFilterRange(range) {
      range = range || this.range; //defaults to existing
      let diff = this.maxWeight - this.minWeight;
      if (diff == 0) this.range = range;
      else {
        this.range = {
          min: (range.min / 100) * diff,
          max: (range.max / 100) * this.maxWeight
        };
      }
      this.filterEntities();
    },
    connectSelected() {
      //uncover all connections between two entities
      if (this.loading) return;
      let selNodes = this.cy.$("node:selected");
      if (selNodes.length != 2) return;
      let e_from = selNodes[0],
        e_to = selNodes[1];
      this.loading = true;
      this.$axios
        .get("/connections", {
          params: {
            from: e_from.id(),
            to: e_to.id(),
            limit: this.limit,
            labels: this.selectedLabels.join()
          }
        })
        .then(res => {
          let nodes = res.data.connections.map(n => this.entityToNode(n));
          let edges = res.data.connections.reduce((acc, r) => {
            return acc.concat([
              this.connectionToEdge({
                from: e_from.id(),
                to: r._id,
                weight: r.from
              }),
              this.connectionToEdge({
                from: r._id,
                to: e_to.id(),
                weight: r.to
              })
            ]);
          }, []);
          this.cy.startBatch();
          {
            //mark as explored before filtering
            e_from.unselect();
            e_to.unselect();
            e_from.data("explored", true);
            e_to.data("explored", true);
            //add nodes and edges to graph
            this.cy.nodes().lock();
            this.cy.add(nodes);
            this.cy.add(edges);

            this.refreshEdgeWeight();
            //reload and filter before running layout for performance
            this.updateFilterRange(); //calls filterEntities after
          }
          this.cy.endBatch();
          this.runLayout("cose", false);
          this.cy.nodes().unlock();
        })
        .catch(e => {
          console.log(e);
          this.$toast.error(
            this.$t("canvas.errors.communication"),
            { x: "right", y: "bottom", timeout: 4000 }
          );
        })
        .finally(() => {
          this.loading = false;
        });
    },
    connectSelectedSingle() {
      //uncover all connections between two entities
      if (this.loading) return;
      let selNodes = this.cy.$("node:selected");
      if (selNodes.length != 2) return;
      let e_from = selNodes[0],
        e_to = selNodes[1];
      this.loading = true;
      this.$axios
        .get("/connection", { params: { from: e_from.id(), to: e_to.id() } })
        .then(res => {
          let weight = res.data.weight;
          let message = `${this.$t("canvas.no_direct_link")} ${e_from.data().text} ${this.$t("canvas.basic.and")} ${
            e_to.data().text
          }`;
          if (weight > 0) {
            message = `${this.$t("canvas.connection_found")} ${weight}`;
            try {
              this.cy.add(
                this.connectionToEdge({
                  from: e_from.id(),
                  to: e_to.id(),
                  weight
                })
              );
            } catch (error) {}
            this.cy.$id(`${e_from.id()},${e_to.id()}`).show();
            this.refreshEdgeWeight();
          }
          this.$toast.info(message, { x: "right", y: "bottom", timeout: 4000 });
          e_from.unselect();
          e_to.unselect();
        })
        .catch(e => {
          console.log(e);
          this.$toast.error(
            this.$t("canvas.errors.communication"),
            { x: "right", y: "bottom", timeout: 4000 }
          );
        })
        .finally(() => {
          this.loading = false;
        });
    },
    intersectSelected() {
      let sn = this.cy.$("node:selected");

      this.cy.startBatch();
      {
        this.cy.nodes().hide();
        sn.show();
        let intersection = sn.reduce(
          (acc, cur) => acc.intersection(cur.outgoers()),
          sn[0].outgoers()
        );
        intersection.show();
      }
      this.cy.endBatch();
    },
    refreshEdgeWeight() {
      //calculate the max and min values for weight
      let weights = this.cy.edges(":visible").map(e => e.data().weight);
      this.minWeight = Math.min(...weights);
      this.maxWeight = Math.max(...weights);
    },
    filterEntities() {
      this.cy.startBatch();
      {
        this.cy.nodes().show();
        let edgesWithin = this.cy.$(
          `edge[weight>=${this.range.min}][weight<=${this.range.max}]`
        );
        edgesWithin
          .connectedNodes()
          .filter(node => this.selectedLabels.indexOf(node.data().label) != -1)
          .show();
        edgesWithin.show();
        let edgesWithout = this.cy.$(
          `edge[weight<${this.range.min}], edge[weight>${this.range.max}]`
        );

        edgesWithout.hide();
        edgesWithout
          .connectedNodes()
          .filter(
            node =>
              !node.data("explored") &&
              node.data("highlight") != 1 &&
              !node.selected() &&
              (node.connectedEdges(":visible").size() === 0 ||
                this.selectedLabels.indexOf(node.data().label) == -1)
          )
          .hide();
        this.cy
          .nodes(
            ":visible:unselected[^explored][highlight!=1], [[degree=0]][highlight!=1]"
          )
          .filter(node => this.selectedLabels.indexOf(node.data().label) == -1)
          .hide();
      }
      this.cy.endBatch();
    },
    invertSelection() {
      let unselected = this.cy.$("node:unselected");
      this.cy.$("node:selected").unselect();
      unselected.select();
      this.updateCountSelectedNodes();
      this.updateCountSelectedEdges();
    },
    expandSelected() {
      let sel = this.cy.$("node:selected");
      if (sel.length != 1) return;
      this.expandEntity(sel[0]);
    },
    expandEntity(e) {
      let el = this.cy.$id(e.id());
      if (el.data("explored")) {
        //if it is explored -> hide
        el.outgoers("[[degree=1]][^explored]").remove();
        el.removeData("explored");
        this.doubleClicked = true;
        {
          el.unselect();
        }
        setTimeout(() => {
          this.doubleClicked = false;
        }, 500);
        return;
      }
      if (this.loading) return;
      this.loading = true;
      this.doubleClicked = true;
      this.$axios
        .get("/expand", {
          params: {
            _id: e.id(),
            limit: this.limit,
            labels: this.selectedLabels.join()
          }
        })
        .then(res => {
          let nodes = res.data.connections.map(r => this.entityToNode(r));
          let edges = res.data.connections.map(r =>
            this.connectionToEdge({
              from: e.id(),
              to: r._id,
              weight: r.weight
            })
          );
          this.cy.startBatch();
          {
            //mark as explored before filtering
            el.data("explored", true);
            el.unselect();
            //add nodes and edges to graph
            this.cy.nodes().lock();
            this.cy.add(nodes);
            this.cy.add(edges);

            this.refreshEdgeWeight();

            //reload and filter before running layout for performance
            // this.updateFilterRange(); //calls filterEntities after
            // this.filterEntities();
          }
          this.cy.endBatch();
          this.runLayout("fCose", false);
          this.cy.nodes().unlock();
          this.$toast.info(`${this.$t("canvas.nodes_found")} ${nodes.length}`, {
            x: "right",
            y: "bottom",
            timeout: 4000
          });
        })
        .catch(e => {
          console.log(e);
          this.$toast.error(
            this.$t("canvas.errors.communication"),
            { x: "right", y: "bottom", timeout: 4000 }
          );
        })
        .finally(() => {
          this.loading = false;
          setTimeout(() => {
            this.doubleClicked = false;
          }, 500);
        });
    },
    runLayout(name, fit) {
      fit = fit || true;
      if (name == "concentric") this.runConcentric(fit);
      else if (name == "cose") this.runCose(fit);
      else if (name == "fCose") this.runfCose(fit);
      else if (name == "bfs") this.runBfs(fit);
    },
    runConcentric(fit) {
      //https://cytoscape.org/cytoscape.js-tutorial-demo/js/index.js
      let calculateCachedCentrality = () => {
        let nodes = this.cy.nodes();

        if (nodes.length > 0 && nodes[0].data("centrality") == null) {
          let centrality = this.cy.elements().closenessCentralityNormalized();
          nodes.forEach(n => n.data("centrality", centrality.closeness(n)));
        }
      };
      calculateCachedCentrality();
      this.cy
        .$(":visible")
        .layout({
          name: "concentric",
          // animate: false,
          randomize: true,
          fit: fit,
          padding: 200,
          nodeDimensionsIncludeLabels: true,
          levelWidth: function(nodes) {
            // calculateCachedCentrality();
            let min = nodes.min(n => n.data("centrality")).value;
            let max = nodes.max(n => n.data("centrality")).value;
            return (max - min) / 5;
          },
          concentric: function(node) {
            // return node
            //   .connectedEdges()
            //   .forEach(e => e.weigth)
            //   .reduce((a, b) => a + b, 0);
            // calculateCachedCentrality();
            return node.data("centrality");
          },
          sweep: (Math.PI * 2) / 3,
          clockwise: true,
          startAngle: (Math.PI * 1) / 6
        })
        .run();
    },
    runCose(fit) {
      this.cy
        .$(":visible")
        .layout({
          name: "cose-bilkent",
          animate: false,
          randomize: true,
          fit: fit,
          padding: 50,
          nodeDimensionsIncludeLabels: true,
          idealEdgeLength: 150,
          nodeRepulsion: 100000,
          edgeElasticity: 0
          // nestingFactor: 1
          // idealEdgeLength: function(edge) {
          //   // Default is: 10
          //   return (1 / edge.data().weight) * 20;
          // }
        })
        .run();
    },
    runfCose(fit) {
      this.cy
        .$(":visible")
        .layout({
          name: "fcose",
          animate: false,
          randomize: true,
          fit: fit,
          padding: 50,
          nodeDimensionsIncludeLabels: true,
          idealEdgeLength: 120,
          nodeRepulsion: 100000,
          uniformNodeDimensions: true,
          edgeElasticity: 0.025
        })
        .run();
    },
    runBfs(fit) {
      this.cy
        .$(":visible")
        .layout({
          name: "breadthfirst",
          animate: false,
          fit: fit,
          padding: 50,
          nodeDimensionsIncludeLabels: true
        })
        .run();
    },
    addNode(e) {
      let current = this.cy.$id(e.data.id);
      if (current.length) {
        this.$toast.info(
            this.$t("canvas.errors.repeated_entity"), {
          x: "right",
          y: "bottom",
          timeout: 4000
        });
        current.show(); //in case it is hidden
        this.focusOnNode(current);
        return;
      }
      this.cy.add(e);
      this.focusOnNode(this.cy.$id(e.data.id));
    },
    focusOnNode(node) {
      node.flashClass("noticeMe", 1000);
      this.cy.animate({ center: { eles: node }, zoom: 1, duration: 1000 });
    },
    connectionToEdge(c) {
      return {
        data: {
          // group: "edges"
          id: [c.from, c.to].sort().join(),
          source: c.from,
          target: c.to,
          weight: c.weight
        }
      };
    },
    entityToNode(e) {
      return {
        data: {
          // group: "nodes"
          id: e._id,
          label: e.label,
          text: e.text
        }
      };
    },
    keydown(e) {
      if (e.key == "Delete") this.deleteSelected();
      if (e.key == "a" && e.ctrlKey) this.selectAll(e);
      if (e.key == "Escape") this.unselectAll();
    },
    deleteSelected() {
      this.cy.$(":selected").remove();
      this.updateCountSelectedNodes();
      this.updateCountSelectedEdges();
    },
    selectAll(e) {
      if (document.activeElement.nodeName != "INPUT") {
        //only if no input is selected
        e.preventDefault();
        this.cy.$(":visible").select();
      }
    },
    unselectAll(e) {
      this.cy.nodes(":selected").unselect();
    },
    downloadPng() {
      saveAs(this.cy.png(), "desarquivo.png");
    },
    downloadJson() {
      let file = new File([JSON.stringify(this.cy.json())], "desarquivo.json", {
        type: "text/plain;charset=utf-8"
      });
      saveAs(file);
    }
  },
  created: function() {
    window.addEventListener("keydown", this.keydown);
  },
  beforeDestroy: function() {
    window.removeEventListener("keydown", this.keydown);
  },
  components: {
    FilterForm,
    NetworkCanvas,
    NewsDrawer
  }
};
</script>
