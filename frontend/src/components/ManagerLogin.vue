<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">Manager Login</div>
                    <div class="card-body">
                        <form @submit.prevent="loginManager">
                            <div class="form-group">
                                <label for="email">Email</label>
                                <input type="email" class="form-control" id="email" v-model="email" required>
                            </div>
                            <div class="form-group">
                                <label for="password">Password</label>
                                <input type="password" class="form-control" id="password" v-model="password" required>
                            </div>
                            <div v-if="error" class="alert alert-danger" role="alert">
                                {{ error }}
                            </div>
                            <button type="submit" class="btn btn-primary">Login</button>
                            <router-link to="/manager-signup" class="btn btn-success">Signup</router-link>
                            
                        </form>
                
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import router from '../router';

export default {
    name: 'ManagerLogin',
    data() {              // ✅ lowercase 'data' not 'Data'
        return {
            email: '',
            password: '',
            error: null
        };
    },                    // ✅ comma not semicolon
    methods: {            // ✅ loginManager must be inside methods
        async loginManager() {
            this.error = null;
            const payload = {
                email: this.email,
                password: this.password
            };
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });
                const result = await response.json();
                if (!response.ok) {
                    this.error = result.message || "Something went wrong";
                } else {
                    if (result.user_role == "manager") {
                        alert("Login successful");
                        localStorage.setItem('token', result.token);
                        this.$router.push('/manager');
                    } else {
                        this.error = "You are not a manager";
                    }
                }
            } catch(error) {
                this.error = "Unable to connect to the server";
            }
        }
    }
}
</script>