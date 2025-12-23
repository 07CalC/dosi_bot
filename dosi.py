import discord
from discord.ext import commands
import os

# Configure intents
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.members = True  # For managing roles
intents.message_content = True  # For processing message commands (optional)

# Set up the bot
bot = commands.Bot(command_prefix="!", intents=intents)
# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def create_roles(ctx, *role_names):
    """Creates multiple roles from a list of role names."""
    try:
        created_roles = []
        for role_name in role_names:
            new_role = await ctx.guild.create_role(name=role_name)
            created_roles.append(new_role.name)

        await ctx.send(f'Roles created successfully: {", ".join(created_roles)}')
    except Exception as e:
        await ctx.send(f'Error creating roles: {e}')


@bot.command()
@commands.has_permissions(manage_roles=True)
async def delete_roles(ctx, *role_names):
    """Deletes multiple roles from a list of role names."""
    try:
        if not role_names:
            await ctx.send("No role names provided!")
            return

        deleted_roles = []
        for role_name in role_names:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role:
                await role.delete()
                deleted_roles.append(role_name)
                print(f"Deleted role: {role_name}")
            else:
                await ctx.send(f'Role not found: {role_name}')

        if deleted_roles:
            await ctx.send(f'Roles deleted successfully: {", ".join(deleted_roles)}')
    except Exception as e:
        await ctx.send(f'Error deleting roles: {e}')
        print(f"Error: {e}")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def assignRole(ctx, role_name, *usernames):
    """Assigns a specific role to a list of usernames."""
    try:
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f'Role not found: {role_name}')
            return

        assigned_users = []
        for username in usernames:
            member = discord.utils.get(ctx.guild.members, name=username)
            if member:
                await member.add_roles(role)
                assigned_users.append(username)
                print(f"Assigned role {role_name} to {username}")
            else:
                await ctx.send(f'User not found: {username}')

        if assigned_users:
            await ctx.send(f'Role {role_name} assigned to: {", ".join(assigned_users)}')
    except Exception as e:
        await ctx.send(f'Error assigning role: {e}')
        print(f"Error: {e}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def remove_role(ctx, role_name, *usernames):
    """Removes a specific role from a list of usernames."""
    try:
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f'Role not found: {role_name}')
            return

        removed_users = []
        for username in usernames:
            member = discord.utils.get(ctx.guild.members, name=username)
            if member:
                await member.remove_roles(role)
                removed_users.append(username)
                print(f"Removed role {role_name} from {username}")
            else:
                await ctx.send(f'User not found: {username}')

        if removed_users:
            await ctx.send(f'Role {role_name} removed from: {", ".join(removed_users)}')
    except Exception as e:
        await ctx.send(f'Error removing role: {e}')
        print(f"Error: {e}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def add_roles_to_channels(ctx, *args):
    """Adds role permissions to multiple channels. Usage: !add_roles_to_channels -r role1 role2 -ch channel1 channel2"""
    try:
        roles = []
        channel_names = []

        # Parse arguments
        args_list = list(args)
        flag = None

        for arg in args_list:
            if arg.startswith("-"):
                flag = arg
            elif flag == "-r":
                roles.append(arg)
            elif flag == "-ch":
                channel_names.append(arg)

        if not roles or not channel_names:
            await ctx.send("Please specify roles (-r) and channels (-ch). Example: !add_roles_to_channels -r role1 role2 -ch announcement discussion")
            return

        # Get role objects
        role_objects = []
        for role_name in roles:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role:
                role_objects.append(role)
            else:
                await ctx.send(f'Role not found: {role_name}')
                return

        # Process each channel (handle multiple channels with same name)
        updated_channel_names = []
        not_found_channels = []
        total_channels_updated = 0
        
        for channel_name in channel_names:
            # Find all channels with this name
            matching_channels = [ch for ch in ctx.guild.channels if ch.name == channel_name]
            
            if matching_channels:
                for channel in matching_channels:
                    for role in role_objects:
                        await channel.set_permissions(role, view_channel=True, send_messages=True)
                        print(f"Added role {role.name} to channel {channel_name} (ID: {channel.id})")
                    total_channels_updated += 1
                updated_channel_names.append(f"{channel_name} ({len(matching_channels)} channel(s))")
            else:
                not_found_channels.append(channel_name)

        if updated_channel_names:
            await ctx.send(f'Roles {", ".join(roles)} added to: {", ".join(updated_channel_names)} - Total: {total_channels_updated} channel(s) updated')
        if not_found_channels:
            await ctx.send(f'Channels not found: {", ".join(not_found_channels)}')
    except Exception as e:
        await ctx.send(f'Error adding roles to channels: {e}')
        print(f"Error: {e}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def delete_roles_from_channels(ctx, *args):
    """Removes role permissions from multiple channels. Usage: !delete_roles_from_channels -r role1 role2 -ch channel1 channel2"""
    try:
        roles = []
        channel_names = []

        # Parse arguments
        args_list = list(args)
        flag = None

        for arg in args_list:
            if arg.startswith("-"):
                flag = arg
            elif flag == "-r":
                roles.append(arg)
            elif flag == "-ch":
                channel_names.append(arg)

        if not roles or not channel_names:
            await ctx.send("Please specify roles (-r) and channels (-ch). Example: !delete_roles_from_channels -r role1 -ch announcement discussion")
            return

        # Get role objects
        role_objects = []
        for role_name in roles:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role:
                role_objects.append(role)
            else:
                await ctx.send(f'Role not found: {role_name}')
                return

        # Process each channel (handle multiple channels with same name)
        updated_channel_names = []
        not_found_channels = []
        total_channels_updated = 0
        
        for channel_name in channel_names:
            # Find all channels with this name
            matching_channels = [ch for ch in ctx.guild.channels if ch.name == channel_name]
            
            if matching_channels:
                for channel in matching_channels:
                    for role in role_objects:
                        await channel.set_permissions(role, overwrite=None)
                        print(f"Removed role {role.name} from channel {channel_name} (ID: {channel.id})")
                    total_channels_updated += 1
                updated_channel_names.append(f"{channel_name} ({len(matching_channels)} channel(s))")
            else:
                not_found_channels.append(channel_name)

        if updated_channel_names:
            await ctx.send(f'Roles {", ".join(roles)} removed from: {", ".join(updated_channel_names)} - Total: {total_channels_updated} channel(s) updated')
        if not_found_channels:
            await ctx.send(f'Channels not found: {", ".join(not_found_channels)}')
    except Exception as e:
        await ctx.send(f'Error removing roles from channels: {e}')
        print(f"Error: {e}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def create_categories_with_channels(ctx, *args):
    """Creates multiple categories with specific channels accessible only to specific roles."""
    try:
        categories = []
        roles = []
        channels = []

        # Use a more robust argument parsing method
        args_list = list(args)
        flag = None

        for arg in args_list:
            if arg.startswith("-"):
                flag = arg
            elif flag == "-m":
                categories.append(arg)
            elif flag == "-r":
                roles.append(arg)
            elif flag == "-ch":
                channels.append(arg)

        if not categories or not roles or not channels:
            await ctx.send("Please specify categories (-m), roles (-r), and channels (-ch). Example: !create_categories_with_channels -m Category1 Category2 -r Role1 Role2 -ch Channel1 Channel2")
            return

        for category_name in categories:
            # Create overwrites for the specified roles
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)
            }
            for role_name in roles:
                role = discord.utils.get(ctx.guild.roles, name=role_name)
                if role:
                    overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
                else:
                    await ctx.send(f'Role not found: {role_name}')
                    return

            # Create the category
            category = await ctx.guild.create_category(category_name, overwrites=overwrites)
            print(f"Created category: {category_name}")

            # Create channels within the category
            created_channels = []
            for channel_name in channels:
                channel = await category.create_text_channel(channel_name)
                created_channels.append(channel.name)
                print(f"Created channel: {channel_name} in category {category_name}")

            await ctx.send(f'Category "{category_name}" with channels "{", ".join(created_channels)}" created for roles "{", ".join(roles)}".')
    except Exception as e:
        await ctx.send(f'Error creating categories or channels: {e}')
        print(f"Error: {e}")

# Run the bot
bot.run(BOT_TOKEN)
