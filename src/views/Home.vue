<template>
  <div>
    <ul>
      <li v-for="county of counties" :key="county">
        <router-link
          :key="county"
          :to="{ path: '/county', query: { name: county.toLowerCase() } }"
          >{{ county }} County</router-link
        >
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Home',

  data: () => ({
    counties: [
      'Bedford',
      'Coffee',
      'Franklin',
      'Giles',
      'Hickman',
      'Lawrence',
      'Lewis',
      'Lincoln',
      'Marshall',
      'Maury',
      'McNairy',
      'Moore',
      'Williamson',
    ],
  }),

  methods: {
    goToCounty(name) {
      this.$router.push({ path: '/county', query: { name } });
    },
  },
};
</script>
