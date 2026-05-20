<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">Admin Login</div>
                    <div class="card-body">
                        <form @submit.prevent="loginAdmin">
                            <div class = "form-group">
                                <label for="email">Email</label>
                                <input type="email" class="form-control" id="email" v-model="email" required>
                            </div>
                            <div class = "form-group">
                                <label for="password">Password</label>
                                <input type="password" class="form-control" id="password" v-model="password" required>
                            </div>
                            <div v-if = "error" class = "alert alert-danger" role = "alert">
                                {{ error }}
                            </div>
                            <button type="submit" class="btn btn-primary">Login</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'AdminLogin',
    data() {
        return {
            email: '',
            password: '',
            error: null   // ✅ remove quotes, null not 'null'
        }
    },
    methods: {
        async loginAdmin() {   // ✅ add async here
            this.error = null;  // ✅ null not 'null'
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
                    if (result.user_role == "admin") {
                        alert("Login successful");
                        localStorage.setItem('token', result.token);
                        this.$router.push('/admin');
                    } else {
                        this.error = "You are not an admin";    
                    }
                }
            } catch(error) {
                this.error = "Unable to connect to the server";
            }
        }
    }
}
</script>