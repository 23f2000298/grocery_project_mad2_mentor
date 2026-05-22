<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">Edit Category</div>
                    <div class="card-body">
                        <form @submit.prevent="editCategory">
                            <div class="form-group">
                                <label for="name">Name</label>
                                <input type="text" class="form-control" id="name" v-model="name" required>
                            </div>

                            <div v-if="error" class="alert alert-danger mt-2" role="alert">
                                {{ error }}
                            </div>

                            <div v-if="success" class="alert alert-success mt-2" role="alert">
                                {{ success }}
                            </div>

                            <button type="submit" class="btn btn-primary mt-3">Update</button>
                            <button type="button" class="btn btn-secondary mt-3 ms-2" @click="$router.push('/admin')">Cancel</button>
                        </form>
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
            name: '',
            error: null,
            success: null
        };
    },
    methods: {
        // ✅ ADDED: pre-fill existing category name on load
        async fetchCategory() {
            try {
                const response = await fetch(`/api/category/${this.$route.params.id}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json'
                    }
                });
                const result = await response.json();
                if (!response.ok) {
                    this.error = result.message || "Error fetching category";
                } else {
                    this.name = result.name;  // ✅ pre-fill the input
                }
            } catch (error) {
                this.error = "Unable to connect to the server";
            }
        },

        async editCategory() {
            this.error = null;
            this.success = null;
            try {
                const response = await fetch(`/api/category/${this.$route.params.id}`, {
                    method: 'PUT',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ name: this.name })
                });
                const result = await response.json();
                if (!response.ok) {
                    this.error = result.message || "Something went wrong";
                } else {
                    this.success = "Category updated successfully!";
                    setTimeout(() => this.$router.push('/admin'), 1500);
                }
            } catch (error) {
                this.error = "Unable to connect to the server";
            }
        }
    },

    mounted() {
        this.fetchCategory();  // ✅ load existing name when page opens
    }
}
</script>