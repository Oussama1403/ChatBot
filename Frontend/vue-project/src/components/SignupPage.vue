<template>
  <div class="signup-page d-flex justify-content-center align-items-center">
    <div class="signup-container glass-card p-5">
      <h2 class="text-center text-muted mb-4">Create an Account</h2>
      <p class="text-center text-muted mb-4">Sign up to get started</p>
      <form @submit.prevent="handleSubmit">
        <div class="form-group mb-4">
          <label for="username" class="form-label">Username</label>
          <input
            type="text"
            id="username"
            class="form-control input-glow"
            v-model="username"
            required
            placeholder="Enter your username"
          />
        </div>

        <div class="form-group mb-4">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            id="password"
            class="form-control input-glow"
            v-model="password"
            required
            placeholder="Enter your password"
          />
        </div>

        <div class="form-group mb-4">
          <label for="confirmPassword" class="form-label">Confirm Password</label>
          <input
            type="password"
            id="confirmPassword"
            class="form-control input-glow"
            v-model="confirmPassword"
            required
            placeholder="Confirm your password"
          />
        </div>

        <button type="submit" class="btn btn-lux w-100" :disabled="isSubmitting">
          Sign Up
        </button>

        <div v-if="errorMessage" class="error-message text-danger mt-3">{{ errorMessage }}</div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      errorMessage: '',
      isSubmitting: false,
    };
  },
  methods: {
    handleSubmit() {
      // Validate the form
      if (this.password !== this.confirmPassword) {
        this.errorMessage = 'Passwords do not match';
        return;
      }

      this.isSubmitting = true;
      this.errorMessage = '';

      axios
        .post('http://127.0.0.1:5000/signup', {
          username: this.username,
          password: this.password,
          confirmPassword: this.confirmPassword
        })
        .then((response) => {
          console.log('Signup successful:', response.data);
          // Redirect or show success message
          this.$router.push('/login');
        })
        .catch((error) => {
          this.errorMessage = error.response.data.message || 'An error occurred';
          console.error('Signup failed:', error);
        })
        .finally(() => {
          this.isSubmitting = false;
        });
    },
  },
};
</script>

<style scoped>
/* Full-screen background with gradient */
.signup-page {
  height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #cb9eff, #aabaff); /* Matches the blue of the chat container */
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Glassmorphism styling for the signup card */
.glass-card {
  background: rgba(254, 226, 255, 0.879);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  max-width: 400px;
  width: 100%;
  color: white;
}

/* Styled form labels */
.form-label {
  font-weight: 500;
  color: rgba(22, 18, 18, 0.8);
}

/* Inputs with glowing focus effect */
.input-glow {
  border-radius: 8px;
  padding: 10px;
  border: none;
  background-color: rgba(255, 255, 255, 0.2);
  color: rgba(22, 18, 18, 0.8);
  transition: box-shadow 0.3s ease, background-color 0.3s ease;
}
.input-glow:focus {
  box-shadow: 0 0 10px rgba(79, 172, 254, 0.8);
  background-color: rgba(255, 255, 255, 0.3);
  outline: none;
}

/* Luxurious button design */
.btn-lux {
  background: linear-gradient(to right, #ff7eb3, #ff758c);
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  padding: 12px 15px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}
.btn-lux:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
}

/* Error message styling */
.error-message {
  font-size: 14px;
  font-weight: bold;
  text-align: center;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .glass-card {
    padding: 20px;
  }
}
</style>
