from django.core.management.base import BaseCommand
from faker import Faker
from apps.accounts.models import User
from apps.profiles.models import Profile, Skill
from apps.projects.models import Project, Tag, Review
import random

class Command(BaseCommand):
    help = "Populate the database with fake data"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Users
        for _ in range(10):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            password = fake.password(length=12)

            # Create a user object
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_email_verified=True,
            )
            # Set the password properly
            user.set_password(password)
            user.save()

            self.stdout.write(f"Created user: {user.email} with password: {password}")

            # Use update_or_create to avoid IntegrityError for Profile
            profile, created = Profile.objects.update_or_create(
                user=user,  # Identify by user
                defaults={
                    'short_intro': fake.sentence(),
                    'bio': fake.paragraph(),
                    'location': fake.city(),
                    'social_github': fake.url(),
                    'social_twitter': fake.url(),
                    'social_linkedin': fake.url(),
                }
            )

            if created:
                self.stdout.write(f"Created profile for user: {user.email}")
            else:
                self.stdout.write(f"Updated profile for user: {user.email}")

            # Create random skills for the profile
            for _ in range(5):
                skill_name = fake.job()
                skill_desc = fake.text(max_nb_chars=200)

                skill = Skill.objects.create(
                    user=profile,  # Reference profile directly
                    name=skill_name,
                    description=skill_desc
                )
                self.stdout.write(f"Added skill {skill_name} to profile: {user.email}")
        
        # Create Tags
        for _ in range(10):
            tag_name = fake.word()
            Tag.objects.create(name=tag_name)
            self.stdout.write(f"Created tag: {tag_name}")
        
        # Create Projects for users
        profiles = Profile.objects.all()
        tags = Tag.objects.all()

        for profile in profiles:
            for _ in range(3):
                project = Project.objects.create(
                    title=fake.sentence(),
                    owner=profile,
                    description=fake.text(),
                    source_link=fake.url(),
                    demo_link=fake.url(),
                    vote_total=random.randint(0, 100),
                    vote_ratio=random.randint(0, 100),
                )

                # Assign random tags to the project
                project.tags.set(random.sample(list(tags), 3))
                project.save()

                self.stdout.write(f"Created project: {project.title} for {profile.user.email}")

                # Create Reviews for the project
                for _ in range(5):
                    reviewer = random.choice(profiles)
                    review_value = random.choice(['up', 'down'])
                    review_content = fake.text()

                    # Use update_or_create to avoid IntegrityError for Review
                    review, created = Review.objects.update_or_create(
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
                        self.stdout.write(f"Updated review for project: {project.title}")
