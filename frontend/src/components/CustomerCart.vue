<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Customer Dashboard</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <router-link to = "/customer" class="nav-link" aria-current="page">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to = "/customer/cart" class="nav-link">Cart</router-link>
                    </li>
                    
                </ul>
                <button class="btn btn-danger" @click="logout">Logout</button>
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">Cart</div>
                    <div class="card-body">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">ID</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Price</th>
                                    <th scope="col">Unit</th>
                                    <th scope="col">Stock</th>
                                    <th scope="col">Category</th>
                                    <th scope="col">Quantity</th>
                                    <th scope="col">Remove</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="item in cartItems" :key="item.id">
                                    <th scope="row">{{ item.id }}</th>
                                    <td>{{ item.name }}</td>
                                    <td>{{ item.price }}</td>
                                    <td>{{ item.unit }}</td>
                                    <td>{{ item.stock }}</td>
                                    <td>{{ item.category_name }}</td>
                                    <td>{{ item.quantity }}</td>
                                    <td>
                                        <button class="btn btn-danger btn-sm" @click="removeFromCart(item.id)">Remove</button>
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
                allCategories: [],
                cartItems: [],
                cartTotal: 0,
                selectCategory: '',

            };
            
        },
        methods:{
            async logout() {
                localStorage.removeItem('token');
                this.$router.push('/');
            },
            async fetchProducts(){
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
            async fetchCategories(){
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
            async addToCart(product_id, quantity) {
                try {
                    const response = await fetch('/api/cart', {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('token')}`,
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ product_id, quantity })
                    });
                    const result = await response.json();
                    if (!response.ok) {
                        this.errorMessage = result.message || "Error adding to cart";
                    } else {
                        alert("Product added to cart");
                        
            
                    }
                } catch (error) {
                    this.errorMessage = "Unable to connect to the server";
                }
            }
        },
        mounted() {
            this.fetchProducts();
            this.fetchCategories();
        }
    }
</script>