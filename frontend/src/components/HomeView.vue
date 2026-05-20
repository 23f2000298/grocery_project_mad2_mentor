<template>
  <div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="card shadow-lg" style="width: 28rem;">
      <div class="card-header bg-success text-white text-center py-3">
        <h4 class="mb-0">🛒 Grocery Store</h4>
      </div>
      <div class="card-body text-center py-4">
        <h5 class="card-title mb-1">Welcome to Grocery Store</h5>
        <p class="text-muted mb-4">Please select your role to continue</p>
        <div class="d-grid gap-3">
          <router-link to="/admin-login" class="btn btn-danger btn-lg">
            🔧 Admin
          </router-link>
          <router-link to="/user-login" class="btn btn-primary btn-lg">
            🛍️ User
          </router-link>
          <router-link to="/manager-login" class="btn btn-warning btn-lg">
            📦 Manager
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    name: 'HomeView',
};
</script>