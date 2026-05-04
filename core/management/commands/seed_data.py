from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Skill, Post, UserProfile
import random

class Command(BaseCommand):
    help = 'Seeds the database with diverse SkillMesh nodes and signals'

    def handle(self, *args, **kwargs):
        self.stdout.write('Initializing Mesh Population Sequence...')

        # 1. Clear existing dummy data if needed (Optional, but good for clean seed)
        # User.objects.exclude(is_superuser=True).delete()
        # Skill.objects.all().delete()

        # 2. Define Protocols (Skills)
        protocols = [
            'Rust', 'Solidity', 'React', 'TypeScript', 'Python', 
            'UI/UX', 'Distributed Systems', 'PostgreSQL', 'Docker',
            'LLMs', 'Tailwind CSS', 'Framer Motion', 'Web3', 'Cybersecurity'
        ]
        
        skill_objs = []
        for p in protocols:
            skill, _ = Skill.objects.get_or_create(name=p)
            skill_objs.append(skill)

        # 3. Define Personas
        personas = [
            {
                'username': 'alex_dev',
                'email': 'alex@example.com',
                'bio': 'Full-stack builder focusing on high-performance infrastructure and distributed protocols. Always open for Rust collaborations.',
                'skills': ['Rust', 'Distributed Systems', 'PostgreSQL'],
                'posts': [
                    {'type': 'general', 'content': 'Just completed a major refactor of the message indexing engine. Latency dropped by 40% using custom Rust buffers.'},
                    {'type': 'open_to_work', 'content': 'Actively looking for senior engineering roles in the Web3 space. Expertise in high-concurrency systems and protocol design.'}
                ]
            },
            {
                'username': 'sarah_design',
                'email': 'sarah@example.com',
                'bio': 'Product designer specializing in complex dashboard systems and motion-heavy user interfaces. Bridging the gap between code and design.',
                'skills': ['UI/UX', 'React', 'Framer Motion', 'Tailwind CSS'],
                'posts': [
                    {'type': 'general', 'content': 'Working on a new design system for SkillMesh. Focus is on high-contrast dark modes and subtle micro-interactions.'},
                    {'type': 'hiring', 'content': 'Hiring: Junior UI Designer to help with component architecture. Must have a deep understanding of Tailwind and Figma. DM for brief.'}
                ]
            },
            {
                'username': 'crypto_node',
                'email': 'crypto@example.com',
                'bio': 'Solidity auditor and smart contract architect. Securing the future of finance one block at a time.',
                'skills': ['Solidity', 'Web3', 'Cybersecurity', 'TypeScript'],
                'posts': [
                    {'type': 'general', 'content': 'Just finished a deep audit for a new DeFi protocol. Found 2 critical vulnerabilities in the reentrancy logic. Stay safe out there.'},
                    {'type': 'hiring', 'content': 'Looking for a Smart Contract Intern who wants to learn the ropes of auditing. 3 month remote project.'}
                ]
            },
            {
                'username': 'ai_architect',
                'email': 'ai@example.com',
                'bio': 'MLE specializing in LLM optimization and RAG pipelines. Building intelligent layers for the mesh.',
                'skills': ['Python', 'LLMs', 'Docker', 'PostgreSQL'],
                'posts': [
                    {'type': 'general', 'content': 'Experimenting with localized LLM inference for privacy-first technical search. The speed vs accuracy trade-off is getting narrower.'},
                    {'type': 'hiring', 'content': 'Hiring: Python Backend Engineer with strong Docker knowledge for an AI-infra startup. Direct signal me for details.'}
                ]
            },
            {
                'username': 'zen_dev',
                'email': 'zen@example.com',
                'bio': 'Minimalist coder. Lover of clean APIs and TypeScript. Building for the long term.',
                'skills': ['TypeScript', 'React', 'Tailwind CSS'],
                'posts': [
                    {'type': 'general', 'content': 'There is a certain beauty in a 100-line script that replaces a 10,000-line library. Simplicity is the ultimate sophistication.'}
                ]
            }
        ]

        for p in personas:
            user, created = User.objects.get_or_create(username=p['username'], email=p['email'])
            if created:
                user.set_password('skillmesh123')
                user.save()
            
            # Update Profile
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.bio = p['bio']
            profile.save()
            
            # Add Skills
            for s_name in p['skills']:
                skill = Skill.objects.get(name=s_name)
                profile.skills.add(skill)
            
            # Create Posts
            for post_data in p['posts']:
                post = Post.objects.create(
                    user=user,
                    content=post_data['content'],
                    post_type=post_data['type']
                )
                # Randomly tag 1-2 skills from user's skills
                post_skills = random.sample(list(profile.skills.all()), min(2, profile.skills.count()))
                post.related_skills.set(post_skills)

        self.stdout.write(self.style.SUCCESS(f'Mesh Population Successful: {len(personas)} nodes synchronized.'))
