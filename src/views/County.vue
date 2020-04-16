<template>
  <div>
    <h1 class="capitalize">{{ $route.query.name }} County</h1>
    <ul>
      <template v-for="cemetery in cemeteries">
        <a :href="cemetery.path" :key="cemetery.name"
          ><li>{{ cemetery.name }}</li></a
        >
      </template>
    </ul>
  </div>
</template>

<script>
import data from '../data/bedford.json';

export default {
  name: 'County',

  computed: {
    cemeteries() {
      return data.cemeteries;
    },
  }
};
</script>
