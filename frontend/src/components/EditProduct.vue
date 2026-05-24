<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Manager Dashboard</a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#" @click="$router.push('/manager')">Back</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">

                <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
                <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

                <div class="card">
                    <div class="card-header">Edit Product</div>
                    <div class="card-body">
                        <div class="row g-2">
                            <div class="col-md-6">
                                <input type="text" class="form-control" placeholder="Name" v-model="product.name">
                            </div>
                            <div class="col-md-6">
                                <input type="text" class="form-control" placeholder="Description" v-model="product.description">
                            </div>
                            <div class="col-md-6">
                                <input type="number" class="form-control" placeholder="Price" v-model="product.price">
                            </div>
                            <div class="col-md-6">
                                <input type="text" class="form-control" placeholder="Unit" v-model="product.unit">
                            </div>
                            <div class="col-md-6">
                                <input type="number" class="form-control" placeholder="Stock" v-model="product.stock">
                            </div>
                            <div class="col-md-6">
                                <select class="form-control" v-model="product.category_id">
                                    <option value="">Select Category</option>
                                    <option v-for="category in categories" :key="category.id" :value="category.id">
                                        {{ category.name }}
                                    </option>
                                </select>
                            </div>
                            <div class="col-md-12 mt-2">
                                <button class="btn btn-primary w-100" @click="updateProduct">Save Changes</button>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            product: {
                name: '',
                description: '',
                price: '',
                unit: '',
                stock: '',
                category_id: '',
            },
            categories: [],
            errorMessage: '',
            successMessage: '',
        };
    },
    methods: {
        async fetchProduct() {
            const id = this.$route.params.id;
            try {
                const response = await fetch(`/api/product/${id}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    },
                });
                const result = await response.json();
                if (!response.ok) {
                    this.errorMessage = result.message || "Error fetching product";
                } else {
                    this.product = result;
                }
            } catch {
                this.errorMessage = "Unable to connect to the server";
            }
        },

        async fetchCategories() {
            try {
                const response = await fetch('/api/category', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    },
                });
                const result = await response.json();
                if (response.ok) this.categories = result;
            } catch {
                this.errorMessage = "Unable to connect to the server";
            }
        },

        async updateProduct() {
            const id = this.$route.params.id;
            try {
                const response = await fetch(`/api/product/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.product),
                });
                const result = await response.json();
                if (!response.ok) {
                    this.errorMessage = result.message || "Error updating product";
                } else {
                    this.successMessage = "Product updated successfully!";
                    setTimeout(() => this.$router.push('/manager'), 1500);
                }
            } catch {
                this.errorMessage = "Unable to connect to the server";
            }
        },
    },

    mounted() {
        this.fetchProduct();
        this.fetchCategories();

        
    },
}
</script>