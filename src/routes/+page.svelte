<script lang="ts">
    import { onMount } from 'svelte';
    import  RatingSystemComponent  from './RatingSystem.svelte';
    import {RatingSystem, Category, Group, Setting} from "$lib/rating/parser.js"
    let ratingSystem: RatingSystem;
  
    // Example JSON data
    const jsonData = {
      name: "MyRatingSystem",
      elements: {
        Art: {
          weight: 40,
          categories: {
            graphics: 40,
            animations: 40,
            other: 20,
          },
        },
        Bruh: {
          weight: 20,
          categories: {
            graphics: 40,
            animations: 40,
            other: 20,
          },
        },
        Music: {
          weight: 20,
        },
        Test: 20,
        __enable_extras: true,
      },
    };
  
    onMount(() => {
      ratingSystem = new RatingSystem("MyRatingSystem");
      ratingSystem.parse(jsonData["elements"]);
  
      try {
        ratingSystem.check_weights();
      } catch (error) {
        console.error('Weight check error:', error);
        // Handle the error as needed
      }
    });
  </script>
  
  <style>
    /* Add your styles here if needed */
  </style>
  
  <RatingSystemComponent {ratingSystem} />
  