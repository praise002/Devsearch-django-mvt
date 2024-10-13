from django.core.management.base import BaseCommand
from apps.accounts.models import User
from apps.profiles.models import Profile, Skill
from apps.projects.models import Project, Tag, Review
import random

class Command(BaseCommand):
    help = "Populate the database with fake data"

    def handle(self, *args, **kwargs):
        # Fetch all existing profiles
        profiles = Profile.objects.all()

        short_intros = [
            "Passionate about technology and committed to excellence.",
            "Creative problem solver with a love for innovation.",
            "Driven by curiosity, always eager to learn and improve.",
            "Detail-oriented and dedicated to delivering top-quality solutions.",
            "A team player who thrives in collaborative environments.",
            "Innovative thinker with a passion for building impactful projects.",
            "Committed to continuous learning and professional growth.",
            "Results-driven with a focus on efficiency and scalability.",
            "Excited about leveraging technology to solve real-world problems.",
            "Motivated by challenges and driven by results."
        ]

        skill_desc = [
            "Skills are the foundation of growth, unlocking new paths to success and innovation.",
            "Mastering skills enables individuals to excel in tasks and contribute meaningfully to teams.",
            "Developing new skills fosters adaptability and opens doors to diverse opportunities.",
            "Continuous skill-building is essential to thriving in today’s fast-evolving technological landscape."
        ]

        project_desc = [
            "This project introduces innovative solutions that address pressing industry challenges.",
            "Crafted with precision, it prioritizes user-centric design while ensuring robust functionality.",
            "Our collaborative process ensured we delivered high-quality results, combining expertise and creativity.",
            "Positive feedback from users confirms the value and effectiveness of our development approach."
        ]

        profile_bio = [
            "I am a passionate technologist, dedicated to driving innovation and solving complex problems.",
            "With extensive experience, I enjoy tackling challenges and continuously expanding my knowledge.",
            "Collaboration and open communication are key to my approach, ensuring success in team environments.",
            "Outside of my professional work, I engage with emerging technologies and contribute to the open-source community.",
            "I believe in using technology to make a lasting, positive impact on the world, and I am driven by this mission."
        ]


        skills_list = [
            "Python Programming",
            "Web Development",
            "Data Analysis",
            "Machine Learning",
            "Project Management",
            "Graphic Design",
            "Digital Marketing",
            "UI/UX Design",
            "Database Management",
            "Cloud Computing",
            "Cybersecurity",
            "Public Speaking",
            "Technical Writing",
            "Agile Methodologies",
            "SEO Optimization",
            "Social Media Management"
        ]

        tags_list = [
            "Innovation",
            "Collaboration",
            "User Experience",
            "Machine Learning",
            "Data Analysis",
            "Web Development",
            "Project Management",
            "Open Source",
            "Community Engagement",
            "Continuous Learning",
            "Agile Development",
            "Digital Transformation",
            "Creative Design",
            "Technical Writing",
            "User-Centric",
            "Sustainable Practices"
        ]
        
        locations = [
            "New York, USA",
            "San Francisco, USA",
            "London, UK",
            "Toronto, Canada",
            "Berlin, Germany",
            "Paris, France",
            "Sydney, Australia",
            "Tokyo, Japan",
            "Singapore",
            "Amsterdam, Netherlands"
        ]
        
        project_titles = [
            "AI-Powered Health Diagnostic System",
            "E-commerce Platform for Local Businesses",
            "Personal Finance Management App",
            "Smart Home Automation Dashboard",
            "Crowdfunding Platform for Nonprofits",
            "Real-Time Collaboration Tool",
            "Online Learning Management System",
            "Blockchain-Based Voting System",
            "SaaS Task and Productivity Tracker",
            "Mobile Fitness and Nutrition Planner"
        ]
        
        review_content_list = [
            "This project is remarkable! It solves a pressing issue effectively.",
            "Impressive work! The user interface is clean and intuitive.",
            "Great concept and execution. This could be a game-changer in its field.",
            "The functionality is top-notch, but the performance could be improved.",
            "A solid project with real-world applications. Well done!",
            "This solution addresses a critical need, and the design is impressive.",
            "Innovative approach with great potential for scalability.",
            "I love the attention to detail in this project. Great job!",
            "The project is well-documented and easy to use, which is a big plus.",
            "Fantastic work! It’s clear a lot of thought went into making this efficient."
        ]

        # Iterate over each profile and populate fields if empty
        for profile in profiles:
            # Populate fields if they are empty
            if not profile.short_intro:
                profile.short_intro = random.choice(short_intros)
                self.stdout.write(f"Populated short_intro for profile of user: {profile.user.email}")

            if not profile.bio:
                profile.bio = random.choice(profile_bio)
                self.stdout.write(f"Populated bio for profile of user: {profile.user.email}")

            if not profile.location:
                profile.location = random.choice(locations)
                self.stdout.write(f"Populated location for profile of user: {profile.user.email}")

            if not profile.social_github:
                profile.social_github = "https://github.com/username"  # Set a meaningful default GitHub link
                self.stdout.write(f"Populated social_github for profile of user: {profile.user.email}")

            if not profile.social_twitter:
                profile.social_twitter = "https://twitter.com/username"  # Set a meaningful default Twitter link
                self.stdout.write(f"Populated social_twitter for profile of user: {profile.user.email}")

            if not profile.social_linkedin:
                profile.social_linkedin = "https://linkedin.com/in/username"  # Set a meaningful default LinkedIn link
                self.stdout.write(f"Populated social_linkedin for profile of user: {profile.user.email}")

            # Save the updated profile
            profile.save()

            # Populate skills
            for _ in range(3):
                skill_name = random.choice(skills_list)  
                skill, created = Skill.objects.get_or_create(
                    user=profile,
                    name=skill_name,
                    defaults={'description': random.choice(skill_desc)}
                )
                if created:
                    self.stdout.write(f"Added skill {skill_name} to profile: {profile.user.email}")
                else:
                    self.stdout.write(f"Skill {skill_name} already exists for profile: {profile.user.email}")

        # Create Tags
        existing_tags = {tag.name for tag in Tag.objects.all()}
        for tag_name in tags_list:
            if tag_name not in existing_tags:
                tag = Tag.objects.create(name=tag_name)
                self.stdout.write(f"Created tag: {tag.name}")
                existing_tags.add(tag_name)

        # Create Projects for profiles
        for profile in profiles:
            for _ in range(3):
                project_title = random.choice(project_titles)
                project, created = Project.objects.get_or_create(
                    title=project_title,
                    owner=profile,
                    defaults={
                        'description': project_desc,
                        'source_link': "https://example.com",  # Use a meaningful link
                        'demo_link': "https://demo.example.com",  # Use a meaningful link
                        'vote_total': random.randint(0, 100),
                        'vote_ratio': random.randint(0, 100),
                    }
                )
                if created:
                    self.stdout.write(f"Created project: {project.title} for {profile.user.email}")
                else:
                    self.stdout.write(f"Project {project.title} already exists for {profile.user.email}")

                # Assign random tags to the project if not already assigned
                for tag in Tag.objects.order_by('?')[:3]:  # Select 3 random tags
                    if tag not in project.tags.all():
                        project.tags.add(tag)
                        self.stdout.write(f"Assigned tag {tag.name} to project: {project.title}")

                # Create Reviews for the project
                for _ in range(5):
                    reviewer = random.choice(profiles)
                    review_value = random.choice(['up', 'down'])
                    review_content = random.choice(review_content_list) 

                    review, created = Review.objects.get_or_create(
                        project=project,
                        reviewer=reviewer,
                        defaults={
                            'value': review_value,
                            'content': review_content
                        }
                    )

                    if created:
                        self.stdout.write(f"Created review for project: {project.title}")
                    else:
                        self.stdout.write(f"Review for project: {project.title} already exists from {reviewer.user.email}")
