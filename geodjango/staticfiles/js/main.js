import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import WKB from 'ol/format/WKB';
import {OSM, Vector as VectorSource} from 'ol/source';
import {Tile as TileLayer, Vector as VectorLayer} from 'ol/layer';

const raster = new TileLayer({
  source: new OSM(),
});

const wkb =
  '0103000000010000000500000054E3A59BC4602540643BDF4F8D1739C05C8FC2F5284C4140EC51B81E852B34C0D578E926316843406F1283C0CAD141C01B2FDD2406012B40A4703D0AD79343C054E3A59BC4602540643BDF4F8D1739C0';

const format = new WKB();

const feature = format.readFeature(wkb, {
  dataProjection: 'EPSG:4326',
  featureProjection: 'EPSG:3857',
});

const vector = new VectorLayer({
  source: new VectorSource({
    features: [feature],
  }),
});

const map = new Map({
  layers: [raster, vector],
  target: 'map',
  view: new View({
    center: [2952104.0199, -3277504.823],
    zoom: 4,
  }),
});
