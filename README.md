# Discord Bot Role Management and Channel Creation - Commands Reference

This document provides a detailed list of available commands, flags, and sample inputs for the Discord bot.

## Table of Commands

| **Command**                           | **Description**                                                | **Flags**                              | **Sample Input** |
|---------------------------------------|----------------------------------------------------------------|----------------------------------------|------------------|
| `!create_roles`                       | Creates one or more roles in the server.                      | None                                   | `!create_roles Admin Moderator Member` |
| `!delete_roles`                       | Deletes one or more roles from the server.                    | None                                   | `!delete_roles Admin Moderator` |
| `!assignRole`                         | Assigns a specific role to one or more users.                 | None                                   | `!assignRole Admin John Jane` |
| `!remove_role`                        | Removes a specific role from one or more users.               | None                                   | `!remove_role Moderator John Jane` |
| `!add_roles_to_channels`              | Adds role permissions to multiple channels at once.           | `-r` (roles), `-ch` (channels)        | `!add_roles_to_channels -r Admin Moderator -ch announcement discussion` |
| `!delete_roles_from_channels`         | Removes role permissions from multiple channels at once.      | `-r` (roles), `-ch` (channels)        | `!delete_roles_from_channels -r Guest -ch private-chat staff-only` |
| `!remove_messaging_permissions`       | Makes specified channels read-only for a role.                | `-r` (role), `-ch` (channels)         | `!remove_messaging_permissions -r Student -ch announcement general-info` |
| `!create_categories_with_channels`    | Creates categories and channels with role-based permissions.  | `-m` (categories), `-r` (roles), `-ch` (channels) | `!create_categories_with_channels -m AdminCategory -r Admin Moderator -ch General Chat` |

## Explanation of Flags

- **`-m` (Categories)**:
  - Specifies the categories to create.
  - **Example**: `-m Category1 Category2`

- **`-r` (Roles)**:
  - Specifies the roles that will have access to the channels in the created categories.
  - **Example**: `-r Role1 Role2`

- **`-ch` (Channels)**:
  - Specifies the channels to create within the specified categories.
  - **Example**: `-ch Channel1 Channel2`

## Channel Permission Management Commands

### `!add_roles_to_channels`
Adds role permissions to multiple existing channels. This command allows you to grant view and send message permissions to one or more roles across multiple channels at once.

**Flags:**
- **`-r` (Roles)**: Specifies the roles to grant permissions to.
  - **Example**: `-r Admin Moderator Guest`
- **`-ch` (Channels)**: Specifies the channels to apply the permissions to.
  - **Example**: `-ch announcement discussion resource`

**Usage:**
```
!add_roles_to_channels -r role1 role2 -ch channel1 channel2 channel3
```

**Examples:**
```
!add_roles_to_channels -r Admin Moderator -ch general announcements help
!add_roles_to_channels -r Member -ch public-chat community
```

**Special Feature:**
- If multiple channels have the same name, this command will update **all** of them.
- Example: If you have 5 channels named "ch1", the command will apply permissions to all 5 channels.
- The bot will report how many channels were updated (e.g., "ch1 (5 channel(s))").

### `!delete_roles_from_channels`
Removes role permissions from multiple existing channels. This command removes the permission overwrites for specified roles from the specified channels.

**Flags:**
- **`-r` (Roles)**: Specifies the roles to remove permissions from.
  - **Example**: `-r Guest Visitor`
- **`-ch` (Channels)**: Specifies the channels to remove the permissions from.
  - **Example**: `-ch private-chat staff-only admin`

**Usage:**
```
!delete_roles_from_channels -r role1 -ch channel1 channel2
```

**Examples:**
```
!delete_roles_from_channels -r Guest -ch private-chat staff-only
!delete_roles_from_channels -r Visitor Temp -ch admin mod-only
```

**Special Feature:**
- Like `!add_roles_to_channels`, this command also handles multiple channels with the same name.
- It will remove permissions from **all** channels matching the provided names.

### `!remove_messaging_permissions`
Makes specified channels read-only for a given role. This command removes the ability to send messages and create threads while preserving the role's ability to view and read messages in the channel.

**Flags:**
- **`-r` (Role)**: Specifies the role to make channels read-only for (single role only).
  - **Example**: `-r Student`
- **`-ch` (Channels)**: Specifies the channels to make read-only.
  - **Example**: `-ch announcement general-info rules`

**Usage:**
```
!remove_messaging_permissions -r role_name -ch channel1 channel2 channel3
```

**Examples:**
```
!remove_messaging_permissions -r Student -ch announcement
!remove_messaging_permissions -r Guest -ch rules general-info announcements
```

**Special Features:**
- **Only modifies existing permissions**: The command only updates channels where the role already has explicit permissions set. If the role doesn't have explicit permissions in a channel, it will be skipped.
- **Supports duplicate channel names**: If you have multiple channels with the same name (e.g., "announcement" in different categories), this command will update **all** of them.
- **Preserves view access**: The role will retain its ability to view and read the channel, but won't be able to send messages or create/participate in threads.
- **Removes these permissions**:
  - Send messages
  - Create public threads
  - Create private threads
  - Send messages in threads

**Use Case Example:**
If you run `!remove_messaging_permissions -r Student -ch announcement`, all channels named "announcement" where the "Student" role has explicit permissions will become read-only for students. They can still see and read announcements, but cannot post or create threads.

## Detailed Example Input

### Command: `!create_categories_with_channels -m AdminCategory -r Admin Moderator -ch General Chat`

- **`-m AdminCategory`**: Creates a category named `AdminCategory`.
- **`-r Admin Moderator`**: Grants access to the `Admin` and `Moderator` roles.
- **`-ch General Chat`**: Creates a channel named `General` under the `AdminCategory`.

---

