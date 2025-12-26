import discord
from discord.ext import commands
import os

# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

# Intents allow the bot to access more events and data
default_intents = discord.Intents.default()
default_intents.guilds = True
default_intents.guild_messages = True
default_intents.members = True  # Required to manage roles

# Set up the bot
bot = commands.Bot(command_prefix="!", intents=default_intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def create_roles(ctx, *role_names):
    """Creates multiple roles from a list of role names."""
    try:
        if not role_names:
            await ctx.send("No role names provided!")
            return

        created_roles = []
        for role_name in role_names:
            new_role = await ctx.guild.create_role(name=role_name)
            created_roles.append(new_role.name)
            print(f"Created role: {role_name}")

        await ctx.send(f'Roles created successfully: {", ".join(created_roles)}')
    except Exception as e:
        await ctx.send(f'Error creating roles: {e}')
        print(f"Error: {e}")

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
async def assign_role(ctx, role_name, *usernames):
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
async def remove_messaging_permissions(ctx, *args):
    """Makes specified channels read-only for a given role (removes send/thread permissions, keeps view permission).
    Only modifies channels where the role already has explicit permissions.
    Supports duplicate channel names - will update all channels with the same name.
    Usage: !remove_messaging_permissions -r role_name -ch channel1 channel2
    Example: !remove_messaging_permissions -r Student -ch announcement general-info"""
    try:
        role_name = None
        channel_names = []

        # Parse arguments
        args_list = list(args)
        flag = None

        for arg in args_list:
            if arg.startswith("-"):
                flag = arg
            elif flag == "-r":
                role_name = arg
                flag = None  # Only take first role name
            elif flag == "-ch":
                channel_names.append(arg)

        if not role_name or not channel_names:
            await ctx.send("Please specify a role (-r) and channels (-ch). Example: !remove_messaging_permissions -r Student -ch announcement")
            return

        # Get role object
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f'Role not found: {role_name}')
            return

        # Process each channel name (handle multiple channels with same name)
        updated_channels = []
        skipped_channels = []
        not_found_channels = set()
        total_channels_updated = 0
        
        for channel_name in channel_names:
            # Find all text channels with this name
            matching_channels = [ch for ch in ctx.guild.text_channels if ch.name == channel_name]
            
            if not matching_channels:
                not_found_channels.add(channel_name)
                continue
            
            for channel in matching_channels:
                # Check if role has explicit permissions in this channel
                role_overwrite = channel.overwrites_for(role)
                
                # Check if the role has any explicit permissions set (not default/None)
                has_explicit_perms = any([
                    role_overwrite.view_channel is not None,
                    role_overwrite.send_messages is not None,
                    role_overwrite.create_public_threads is not None,
                    role_overwrite.create_private_threads is not None,
                    role_overwrite.send_messages_in_threads is not None
                ])
                
                if has_explicit_perms:
                    # Role has explicit permissions, keep view_channel but deny messaging
                    # Get current overwrites to preserve view_channel setting
                    current_overwrites = channel.overwrites_for(role)
                    
                    await channel.set_permissions(
                        role,
                        view_channel=current_overwrites.view_channel if current_overwrites.view_channel is not None else True,
                        send_messages=False,
                        create_public_threads=False,
                        create_private_threads=False,
                        send_messages_in_threads=False
                    )
                    updated_channels.append(f"{channel.name} (ID: {channel.id})")
                    total_channels_updated += 1
                    print(f"Made channel {channel.name} (ID: {channel.id}) read-only for role {role.name}")
                else:
                    # Role doesn't have explicit permissions, skip it
                    skipped_channels.append(f"{channel.name} (ID: {channel.id})")
                    print(f"Skipped channel {channel.name} (ID: {channel.id}) - role {role.name} has no explicit permissions")

        # Send feedback
        response_parts = []
        
        if updated_channels:
            response_parts.append(f'Made {total_channels_updated} channel(s) read-only for role "{role_name}": {", ".join(updated_channels)}')
        
        if skipped_channels:
            response_parts.append(f'Skipped {len(skipped_channels)} channel(s) where role has no explicit permissions: {", ".join(skipped_channels)}')
        
        if not_found_channels:
            response_parts.append(f'Channels not found: {", ".join(not_found_channels)}')
        
        if not response_parts:
            await ctx.send(f'No channels were updated.')
        else:
            # Send response in chunks if too long
            full_response = '\n'.join(response_parts)
            if len(full_response) > 2000:
                for part in response_parts:
                    await ctx.send(part)
            else:
                await ctx.send(full_response)
                
    except Exception as e:
        await ctx.send(f'Error making channels read-only: {e}')
        print(f"Error: {e}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def create_category_with_channels(ctx, category_name, *args):
    """Creates a category with specific channels accessible only to specific roles."""
    try:
        roles = []
        text_channels = []
        audio_channels = []

        # Parse arguments for roles (-r), text channels (-ch), and audio channels (-a)
        args_list = list(args)
        while args_list:
            arg = args_list.pop(0)
            if arg == "-r":
                while args_list and not args_list[0].startswith("-"):
                    roles.append(args_list.pop(0))
            elif arg == "-ch":
                while args_list and not args_list[0].startswith("-"):
                    text_channels.append(args_list.pop(0))
            elif arg == "-a":
                while args_list and not args_list[0].startswith("-"):
                    audio_channels.append(args_list.pop(0))

        if not roles or (not text_channels and not audio_channels):
            await ctx.send("Please specify roles (-r), and at least one type of channel (-ch or -a). Example: !create_category_with_channels category_name -r Role1 Role2 -ch TextChannel1 -a VoiceChannel1")
            return

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

        # Create text channels within the category
        created_text_channels = []
        for channel_name in text_channels:
            channel = await category.create_text_channel(channel_name)
            created_text_channels.append(channel.name)
            print(f"Created text channel: {channel_name} in category {category_name}")

        # Create audio channels within the category
        created_audio_channels = []
        for channel_name in audio_channels:
            channel = await category.create_voice_channel(channel_name)
            created_audio_channels.append(channel.name)
            print(f"Created audio channel: {channel_name} in category {category_name}")

        await ctx.send(f'Category "{category_name}" with text channels "{", ".join(created_text_channels)}" and audio channels "{", ".join(created_audio_channels)}" created for roles "{", ".join(roles)}".')
    except Exception as e:
        await ctx.send(f'Error creating category or channels: {e}')
        print(f"Error: {e}")

# Run the bot
bot.run(BOT_TOKEN)
