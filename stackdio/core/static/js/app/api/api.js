define(["app/api/InstanceSizes", 
        "app/api/Profiles", 
        "app/api/Accounts", 
        "app/api/ProviderTypes", 
        "app/api/Roles", 
        "app/api/Snapshots", 
        "app/api/StackHosts", 
        "app/api/Stacks"
        ], 
    function (InstanceSizes, Profiles, Accounts, ProviderTypes, Roles, Snapshots, StackHosts, Stacks) {

    return {
        InstanceSizes: InstanceSizes,
        Profiles:      Profiles,
        Accounts:      Accounts,
        ProviderTypes: ProviderTypes,
        Roles:         Roles,
        Snapshots:     Snapshots,
        StackHosts:     StackHosts,
        Stacks:        Stacks
    }
});