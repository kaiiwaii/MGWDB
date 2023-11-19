<script lang="ts">
    import { onMount } from 'svelte';
    import  RatingSystemComponent  from './RatingSystem.svelte.js';
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
            let groups = ratingSystem.check_global_weights();
            ratingSystem.check_local_weights(groups);
        } catch (error) {
            console.error('Weight check error:', error);

            if (error.name === "GlobalWeightError") {
            globalWeightError = true;
            } else if (error.name === "LocalWeightError") {
            globalWeightError = false;
            localWeightError = true;
            localWeightErrorValue = error.value;
            }
        }
    });

let globalWeightError = false;
let localWeightError = false;
let localWeightErrorValue = 0;
  </script>
  
  <style>
    /* Add your styles here if needed */
  </style>
  
  <RatingSystemComponent {ratingSystem} />
  