<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Admin Dashboard</a>
        </div>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="#">Home</a>
                </li>
                <li class="nav-item">
                    <router-link to="/create-category" class="nav-link">Create Category</router-link>
                </li>
                <li>
                    <router-link to="/export" class="nav-link">Export</router-link>
                </li>
                <li>
                    <a class="nav-link" href="#" @click="logout">Logout</a>
                </li>
            </ul>
        </div>
    </nav>

    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-10">
                <div class="card">
                    <div class="card-header">All Managers</div>
                    <div class="card-body">
                        <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">ID</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Email</th>
                                    <th scope="col">Status</th>
                                    <th scope="col">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="manager in managers" :key="manager.id">
                                    <th scope="row">{{ manager.id }}</th>
                                    <td>{{ manager.name }}</td>
                                    <td>{{ manager.email }}</td>
                                    <td>{{ manager.status }}</td>
                                    <td>
                                        <button
                                            v-if="manager.status == 'pending'"
                                            @click="approveManager(manager.id)"
                                            class="btn btn-success btn-sm">
                                            Approve
                                        </button>
                                        <span v-else class="text-muted">—</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-10">
                <div class="card">
                    <div class="card-header">All Categories</div>
                    <div class="card-body">
                        <table v-if = "categories.length > 0" class="table">
                            <thead>
                                <tr>
                                    <th scope="col">ID</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Delete</th>
                                    <th scope="col">Edit</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="category in categories" :key="category.id">
                                    <th scope="row">{{ category.id }}</th>
                                    <td>{{ category.name }}</td>
                                    <td>
                                        <button class="btn btn-danger btn-sm" @click="deleteCategory(category.id)">Delete</button>
                                    </td>
                                    <td>
                                        <router-link :to="`/edit-category/${category.id}`" class="btn btn-primary btn-sm">Edit</router-link>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <p v-else> No categories found.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-10">
        <div class="card">
          <div class="card-header">Category Request</div>
          <div class="card-body">
            <table class="table">
              <thead>
                <tr>
                  <th scope="col">Category ID</th>
                  <th scope="col">Name</th>
                  <th scope="col">Action</th>
                  <th scope="col">Status</th>
                  <th scope="col">Actions</th>
                </tr>
              </thead>
              <tbody>
                <!-- FIX 6: iterate over categoryRequest, not categories -->
                <tr v-for="(request, index) in categoryRequest" :key="index">
                  <td>{{ request.category_id }}</td>
                  <td>{{ request.name }}</td>
                  <td>{{ request.action }}</td>
                  <td>{{ request.status }}</td>
                  <td>
                    <button v-if="request.status == 'pending'" @click="approveCategoryRequest(request.id)" class="btn btn-success btn-sm">Approve</button>
                    <button v-if="request.status == 'pending'" @click="rejectCategoryRequest(request.id)" class="btn btn-danger btn-sm">Reject</button>

                    <span v-else class="text-muted">—</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { provide } from 'vue';

export default {
    data() {
        return {
            managers: [],
            errorMessage: null,
            Products: [],
            categories: [],
            categoryRequest: [],
            newProduct:{
                name: '',
                price: '',
                description: '',
                category_id: '',
                unit: '',
                stock: '',
                sold: '',
                manager_id: '',
            }
        };
    },
    methods: {
        async logout() {
            localStorage.removeItem('token');
            this.$router.push('/');
        },


        async approveCategoryRequest(id) {
            try {
                const response = await fetch(`/api/category/request/action`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        request_id = id,
                        action: 'approve',
                    }),
                });
                const result = await response.json();
                if (!response.ok) {
                    this.errorMessage = result.message || "Error approving category request";
                } else {
                    alert("Category request approved successfully");
                    this.fetchCategoryRequest();
                }
            } catch (error) {
                this.errorMessage = "Unable to connect to the server";
            }
        },
        async fetchCategoryRequest() {
        try {
            const response = await fetch('/api/category/request', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                },
            });
            const result = await response.json();
            if (!response.ok) {
                this.errorMessage = result.message || "Error fetching category requests";
            } else {
                // FIX: extract the array from the correct key
                this.categoryRequest = result.category_request;
            }
        } catch (error) {
            this.errorMessage = "Unable to connect to the server";
        }
    },
        async fetchManagers() {
            try {
                const token = localStorage.getItem('token');
                console.log("Token:", token);           // ✅ check token exists

                const response = await fetch('/api/manager', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                console.log("Status:", response.status); // ✅ check response status
                const result = await response.json();
                console.log("Result:", result);           // ✅ check what Flask returns

                if (!response.ok) {
                    this.errorMessage = result.message || "Error fetching managers";
                    if (response.status === 403) {
                        this.$router.push('/admin-login'); // ✅ kick out if wrong role
                    }
                } else {
                    this.managers = result;
                }
            } catch (error) {
                this.errorMessage = "Unable to connect to the server";
            }
        },
        async approveManager(id) {
            try {
                const response = await fetch(`/api/manager/${id}`, {
                    method: 'PATCH',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json',
                    },
                });
                if (response.ok) {
                    alert("Manager approved successfully");
                    this.fetchManagers();
                } else {
                    const result = await response.json();
                    alert(result.message || "Error approving manager");
                }
            } catch (error) {
                this.errorMessage = "Unable to connect to the server";
            }
        },
        async fetchCategories() {
            try {
                const response = await fetch('/api/category', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json',
                    },
                });
                const result = await response.json();
                if (!response.ok) {
                    this.errorMessage = result.message || "Error fetching categories";
                } else {
                    this.categories = result;
                }
            } catch (error) {
                this.errorMessage = "Unable to connect to the server";
            }
        },
        async deleteCategory(id) {
            try {
                const response = await fetch(`/api/category/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json',
                    },
                });
                if (response.ok) {
                    alert("Category deleted successfully");
                    this.fetchCategories();
                } else {
                    const result = await response.json();
                    alert(result.message || "Error deleting category");
                }
            } catch (error) {
                alert("Unable to connect to the server");
            }
        },
    },
    mounted() {
        this.fetchManagers();
        this.fetchCategories();
        this.fetchCategoryRequest();
    },
}
</script>