# Pulumi Patterns Reference

Complete guide to Pulumi component design using TypeScript.

## Project Structure

```
pulumi/
├── index.ts              # Entry point
├── package.json
├── tsconfig.json
├── Pulumi.yaml           # Project config
├── Pulumi.dev.yaml       # Dev stack config
├── Pulumi.prod.yaml      # Prod stack config
└── components/
    ├── api-service.ts
    ├── database.ts
    └── networking.ts
```

## Component Resource Pattern

### Basic Component
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

export interface ApiServiceArgs {
  name: string;
  environment: string;
  containerImage: pulumi.Input<string>;
  cpu?: number;
  memory?: number;
  desiredCount?: number;
  vpcId: pulumi.Input<string>;
  subnetIds: pulumi.Input<string>[];
  securityGroupIds?: pulumi.Input<string>[];
  tags?: pulumi.Input<{ [key: string]: pulumi.Input<string> }>;
}

export class ApiService extends pulumi.ComponentResource {
  public readonly serviceName: pulumi.Output<string>;
  public readonly taskDefinitionArn: pulumi.Output<string>;
  public readonly securityGroupId: pulumi.Output<string>;

  constructor(
    name: string,
    args: ApiServiceArgs,
    opts?: pulumi.ComponentResourceOptions
  ) {
    super("genesis:aws:ApiService", name, {}, opts);

    const defaultResourceOptions: pulumi.ResourceOptions = { parent: this };

    // Security Group
    const securityGroup = new aws.ec2.SecurityGroup(
      `${name}-sg`,
      {
        vpcId: args.vpcId,
        description: `Security group for ${args.name}`,
        ingress: [
          {
            fromPort: 8080,
            toPort: 8080,
            protocol: "tcp",
            cidrBlocks: ["0.0.0.0/0"],
          },
        ],
        egress: [
          {
            fromPort: 0,
            toPort: 0,
            protocol: "-1",
            cidrBlocks: ["0.0.0.0/0"],
          },
        ],
        tags: args.tags,
      },
      defaultResourceOptions
    );

    // ECS Cluster
    const cluster = new aws.ecs.Cluster(
      `${name}-cluster`,
      {
        name: `${args.name}-${args.environment}`,
        tags: args.tags,
      },
      defaultResourceOptions
    );

    // Task Definition
    const taskDefinition = new aws.ecs.TaskDefinition(
      `${name}-task`,
      {
        family: `${args.name}-${args.environment}`,
        networkMode: "awsvpc",
        requiresCompatibilities: ["FARGATE"],
        cpu: String(args.cpu ?? 256),
        memory: String(args.memory ?? 512),
        containerDefinitions: pulumi
          .output(args.containerImage)
          .apply((image) =>
            JSON.stringify([
              {
                name: args.name,
                image: image,
                portMappings: [{ containerPort: 8080 }],
                essential: true,
              },
            ])
          ),
      },
      defaultResourceOptions
    );

    // ECS Service
    const service = new aws.ecs.Service(
      `${name}-service`,
      {
        name: `${args.name}-${args.environment}`,
        cluster: cluster.arn,
        taskDefinition: taskDefinition.arn,
        desiredCount: args.desiredCount ?? (args.environment === "prod" ? 3 : 1),
        launchType: "FARGATE",
        networkConfiguration: {
          subnets: args.subnetIds,
          securityGroups: args.securityGroupIds ?? [securityGroup.id],
          assignPublicIp: true,
        },
      },
      defaultResourceOptions
    );

    this.serviceName = service.name;
    this.taskDefinitionArn = taskDefinition.arn;
    this.securityGroupId = securityGroup.id;

    this.registerOutputs({
      serviceName: this.serviceName,
      taskDefinitionArn: this.taskDefinitionArn,
      securityGroupId: this.securityGroupId,
    });
  }
}
```

## Using Components

### index.ts
```typescript
import * as pulumi from "@pulumi/pulumi";
import { ApiService } from "./components/api-service";
import { Database } from "./components/database";

const config = new pulumi.Config();
const environment = pulumi.getStack();

// Get config values
const vpcId = config.require("vpcId");
const subnetIds = config.requireObject<string[]>("subnetIds");
const containerImage = config.require("containerImage");

// Create database
const database = new Database("main-db", {
  name: "myapp",
  environment,
  instanceClass: environment === "prod" ? "db.r6g.large" : "db.t3.micro",
  vpcId,
  subnetIds,
});

// Create API service
const apiService = new ApiService("api", {
  name: "myapp-api",
  environment,
  containerImage,
  cpu: environment === "prod" ? 512 : 256,
  memory: environment === "prod" ? 1024 : 512,
  desiredCount: environment === "prod" ? 3 : 1,
  vpcId,
  subnetIds,
  tags: {
    Environment: environment,
    Project: "myapp",
  },
});

// Exports
export const apiServiceName = apiService.serviceName;
export const databaseEndpoint = database.endpoint;
```

## Stack Configuration

### Pulumi.yaml
```yaml
name: myapp
runtime: nodejs
description: My application infrastructure
```

### Pulumi.dev.yaml
```yaml
config:
  aws:region: us-east-1
  myapp:vpcId: vpc-123456
  myapp:subnetIds:
    - subnet-abc
    - subnet-def
  myapp:containerImage: myapp:dev
```

### Pulumi.prod.yaml
```yaml
config:
  aws:region: us-west-2
  myapp:vpcId: vpc-789012
  myapp:subnetIds:
    - subnet-ghi
    - subnet-jkl
  myapp:containerImage: myapp:v1.2.3
```

## Advanced Patterns

### Transformations
```typescript
// Apply tags to all resources
pulumi.runtime.registerStackTransformation((args) => {
  if (args.type.startsWith("aws:")) {
    args.props["tags"] = {
      ...args.props["tags"],
      ManagedBy: "pulumi",
      Stack: pulumi.getStack(),
    };
  }
  return { props: args.props, opts: args.opts };
});
```

### Dynamic Providers
```typescript
const myProvider = new pulumi.dynamic.ResourceProvider({
  async create(inputs) {
    // Custom create logic
    return { id: "unique-id", outs: { result: "created" } };
  },
  async delete(id, outs) {
    // Custom delete logic
  },
});
```

### Component Aliases
```typescript
const service = new ApiService("api", args, {
  aliases: [{ name: "old-api-name" }],
});
```

## Best Practices

### 1. Type Everything
```typescript
interface DatabaseArgs {
  name: string;
  instanceClass: pulumi.Input<string>;
  // ...
}
```

### 2. Use ComponentResource
- Groups related resources
- Provides logical naming
- Enables proper dependency tracking

### 3. Register Outputs
```typescript
this.registerOutputs({
  endpoint: this.endpoint,
  arn: this.arn,
});
```

### 4. Handle Secrets
```typescript
const dbPassword = config.requireSecret("dbPassword");
// Outputs are automatically marked sensitive
```
