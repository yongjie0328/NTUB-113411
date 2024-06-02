document.addEventListener("DOMContentLoaded", function() {
    // Add fade-in effect to text blocks
    document.querySelectorAll('.text-block').forEach(function(el) {
        el.style.opacity = 0;
        setTimeout(function() {
            el.style.opacity = 1;
        }, 500);
    });

    // Add hover effect to cards
    document.querySelectorAll('.card').forEach(function(el) {
        el.addEventListener('mouseover', function() {
            this.style.transform = 'scale(1.1)';
        });
        el.addEventListener('mouseout', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Add collapsible behavior
    document.querySelectorAll('.collapsible').forEach(function(el) {
        el.addEventListener('click', function() {
            this.classList.toggle('active');
            let content = this.nextElementSibling;
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });
    });

    // Add fade-out effect on scroll for strategy table
    const strategyTable = document.querySelector('#strategies .table');
    window.addEventListener('scroll', function() {
        if (window.scrollY + window.innerHeight >= strategyTable.offsetTop) {
            strategyTable.style.opacity = 0;
        } else {
            strategyTable.style.opacity = 1;
        }
    });

    // Add scroll effect for smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add slide-in effect for sections
    const sections = document.querySelectorAll('section');
    const options = {
        threshold: 0.1
    };
    const observer = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                return;
            }
            entry.target.classList.add('slide-in');
            observer.unobserve(entry.target);
        });
    }, options);
    sections.forEach(section => {
        observer.observe(section);
    });
});


function toggleText(button) {
    var moreText = button.nextElementSibling;
    if (moreText.style.display === "none" || moreText.style.display === "") {
        moreText.style.display = "block";
        button.textContent = "Show less";
    } else {
        moreText.style.display = "none";
        button.textContent = "Read more";
    }
}

window.addEventListener('scroll', function() {
    var sections = document.querySelectorAll('section');
    sections.forEach(function(section) {
        var rect = section.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom >= 0) {
            section.classList.remove('fade-out');
        } else {
            section.classList.add('fade-out');
        }
    });
});

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

document.getElementById("defaultOpen").click();