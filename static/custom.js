document.addEventListener("DOMContentLoaded", () => {
    const commentForms = document.querySelectorAll("form");
    commentForms.forEach(form => {
        form.addEventListener("submit", () => {
            toastr.info("Submitting your comment...");
        });
    });
});
