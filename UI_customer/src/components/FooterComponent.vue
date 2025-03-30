<template>
  <footer class="w-full bg-slate text-white py-8 px-4 mt-auto">
    <div class="nom-container flex flex-col md:flex-row justify-between items-center">
      <div class="mb-4 md:mb-0">
        <h3 class="text-lg font-bold mb-2">NomNomBox</h3>
        <p class="text-sm text-muted-foreground">&copy; 2025 NomNomBox. All rights reserved.</p>
      </div>
      
      <div class="flex flex-col md:flex-row gap-4 md:gap-8">
        <div>
          <h4 class="text-secondary font-medium mb-2">Links</h4>
          <ul class="space-y-1">
            <li><a href="#" class="text-sm text-muted-foreground hover:text-white transition-colors">About Us</a></li>
            <li><a href="#contact" class="text-sm text-muted-foreground hover:text-white transition-colors">Contact</a></li>
            <li><a href="#faq" class="text-sm text-muted-foreground hover:text-white transition-colors">FAQ</a></li>
          </ul>
        </div>
        
        <div>
          <h4 class="text-secondary font-medium mb-2">Contact</h4>
          <ul class="space-y-1">
            <li class="text-sm text-muted-foreground">Email: hello@nomnombox.com</li>
            <li class="text-sm text-muted-foreground">Phone: (123) 456-7890</li>
          </ul>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'FooterComponent'
};
</script>