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
                        <router-link to = "/customer" class="nav-link active" aria-current="page">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/customer/cart" class="nav-link">Cart</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/customer/orders" class="nav-link">Orders</router-link>
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
                                    <th>Quantity</th>
                                    <th>Add to Cart</th>
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
                                        <input type="number" class="form-control" placeholder="Quantity" v-model="product.quantity">
                                    </td>
                                    <td>
                                    <button class="btn btn-primary btn-sm" @click="addToCart(product.id, product.quantity)">Add to Cart</button>                                    </td>
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
                    if (!quantity || quantity < 1) {
                        alert("Please enter a valid quantity");
                        return;
                    }
                    try {
                        const response = await fetch('/api/cart', {
                            method: 'POST',
                            headers: {
                                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ product_id, quantity: parseInt(quantity) }) // ✅ send as int
                        });
                        const result = await response.json();
                        if (!response.ok) {
                            alert(result.message || "Error adding to cart");
                        } else {
                            alert("Product added to cart successfully");
                        }
                    } catch (error) {
                        alert("Unable to connect to the server");
                    }
                }
        },
        mounted() {
            this.fetchProducts();
            this.fetchCategories();
        }
    }
</script>