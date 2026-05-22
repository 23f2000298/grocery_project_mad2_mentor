<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Manager Dashboard</a>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#" @click="logout">Logout</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-10">

                <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

                <div class="card mb-4">
                    <div class="card-header">Add New Product</div>
                    <div class="card-body">
                        <div class="row g-2">
                            <div class="col-md-4">
                                <input type="text" class="form-control" placeholder="Name" v-model="newProduct.name">
                            </div>
                            <div class="col-md-4">
                                <input type="text" class="form-control" placeholder="Description" v-model="newProduct.description">
                            </div>
                            <div class="col-md-4">
                                <input type="number" class="form-control" placeholder="Price" v-model="newProduct.price">
                            </div>
                            <div class="col-md-4">
                                <input type="text" class="form-control" placeholder="Unit" v-model="newProduct.unit">
                            </div>
                            <div class="col-md-4">
                                <input type="number" class="form-control" placeholder="Stock" v-model="newProduct.stock">
                            </div>
                            <div class="col-md-4">
                                <select class="form-control" v-model="newProduct.category_id">
                                    <option value="">Select Category</option>
                                    <option v-for="category in categories" :key="category.id" :value="category.id">
                                        {{ category.name }}
                                    </option>
                                </select>
                            </div>
                            <div class="col-md-12">
                                <button class="btn btn-success" @click="addProduct">Add Product</button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">All Products</div>
                    <div class="card-body">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Name</th>
                                    <th>Price</th>
                                    <th>Unit</th>
                                    <th>Stock</th>
                                    <th>Category</th>
                                    <th>Delete</th>
                                    <th>Edit</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="product in allProducts" :key="product.id">
                                    <td>{{ product.id }}</td>
                                    <td>{{ product.name }}</td>
                                    <td>{{ product.price }}</td>
                                    <td>{{ product.unit }}</td>
                                    <td>{{ product.stock }}</td>
                                    <td>{{ product.category_name }}</td>
                                    <td>
                                        <button class="btn btn-danger btn-sm" @click="deleteProduct(product.id)">Delete</button>
                                    </td>
                                    <td>
                                        <button class="btn btn-primary btn-sm" @click="editProduct(product.id)">Edit</button>
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
export default {
    data() {
        return {
            allProducts: [],
            categories: [],
            errorMessage: '',
            newProduct: {
                name: '',
                description: '',
                price: '',
                unit: '',
                stock: '',
                category_id: '',
            }
        };
    },
    methods: {
        async logout() {
            localStorage.removeItem('token');
            this.$router.push('/');
        },

        async fetchProducts() {
            try {
                const response = await fetch('/api/product', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json',
                    },
                });
                const result = await response.json();
                if (!response.ok) {
                    this.errorMessage = result.message || "Error fetching products";
                } else {
                    this.allProducts = result.products;
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

        async addProduct() {
            try {
                const response = await fetch('/api/product', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        name: this.newProduct.name,
                        description: this.newProduct.description,
                        price: this.newProduct.price,
                        unit: this.newProduct.unit,
                        stock: this.newProduct.stock,
                        category_id: this.newProduct.category_id,
                    }),
                });
                const result = await response.json();
                if (!response.ok) {
                    this.errorMessage = result.message || "Something went wrong";
                } else {
                    alert("Product added successfully");
                    this.newProduct = { name: '', description: '', price: '', unit: '', stock: '', category_id: '' };
                    this.fetchProducts();
                }
            } catch (error) {
                this.errorMessage = "Unable to connect to the server";
            }
        },

        async deleteProduct(id) {
            try {
                const response = await fetch(`/api/product/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json',
                    },
                });
                if (response.ok) {
                    alert("Product deleted successfully");
                    this.fetchProducts();
                } else {
                    const result = await response.json();
                    alert(result.message || "Error deleting product");
                }
            } catch (error) {
                alert("Unable to connect to the server");
            }
        },

        // ✅ FIXED: moved inside methods block
        editProduct(id) {
            this.$router.push(`/edit-product/${id}`);
        },
    },

    mounted() {
        this.fetchProducts();
        this.fetchCategories();
    },
}
</script>