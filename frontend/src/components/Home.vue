<template>
    <div class="container mt-5">
        <h1 class="text-center">Latest Articles</h1>
        <div v-if="loading" class="text-center">
            <p>Loading articles...</p>
        </div>
        <div v-if="error" class="text-center text-danger">
            <p>{{ error }}</p>
        </div>
        <div v-if="!loading && articles.length > 0" class="row justify-content-center">
            <div v-for="article in articles" :key="article.id" class="col-12 col-md-8 mb-4">
            <div class="card shadow-sm p-3 bg-white rounded py-4">
                <div class="card-body text-center">
                <h5 class="card-title">{{ article.title }}</h5>
                <p class="card-text">{{ article.summary }}</p>
                <button @click="navigateToArticle(article.id)" class="btn btn-primary mx-2">Chat</button>
                <a :href="article.url" class="btn btn-outline-primary" target="_blank">View Article</a>
                </div>
            </div>
            </div>
        </div>
    </div>
  </template>
  
  <script>
  import { useRouter } from 'vue-router';
  import { onMounted, ref, getCurrentInstance } from 'vue';

  export default {
    setup() {
      const articles = ref([]);
      const loading = ref(false);
      const error = ref(null);

      const { proxy } = getCurrentInstance();
      const router = useRouter();

      const fetchArticles = async () => {
        loading.value = true;
        proxy.$axios
        .get("/get_posts")
        .then((response) => {
            articles.value = response.data;
        })
        .catch((err) => {
            console.error("Error:", err);
            error.value = "Error fetching articles, Please try again later.";
        }).finally(() => {
            loading.value = false;
        });
      };

      const navigateToArticle = (id) => {
        console.log("Navigating to article with id:", id);
        console.log(router)
        router.push({ name: "Article", params: { id } });
      };

      onMounted(() => {
        fetchArticles();
      });
  
      return {
        articles,
        loading,
        error,
        navigateToArticle
      };
    },
  };
  </script>
  
  <style scoped>
  .card {
    max-width: 100%;
  }
  
  .card-title {
    font-size: 1.5rem;
  }
  
  .card-text {
    font-size: 1rem;
  }
  
  .container {
    padding: 20px;
  }
  </style>