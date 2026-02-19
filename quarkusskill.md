# Java Quarkus Enterprise Development Skill

## Overview
This skill provides comprehensive guidance for building production-ready, enterprise-grade Java applications using Quarkus framework. It covers architecture patterns, security, observability, performance optimization, testing strategies, and deployment best practices.

## Table of Contents
1. [Project Setup & Structure](#project-setup--structure)
2. [Architecture Patterns](#architecture-patterns)
3. [Exception Handling](#exception-handling)
4. [Security & Authentication](#security--authentication)
5. [External API Integration](#external-api-integration)
6. [Database & Persistence](#database--persistence)
7. [Messaging & Events](#messaging--events)
8. [Caching Strategies](#caching-strategies)
9. [Observability & Monitoring](#observability--monitoring)
10. [Testing Strategies](#testing-strategies)
11. [Performance Optimization](#performance-optimization)
12. [Configuration Management](#configuration-management)
13. [Containerization & Deployment](#containerization--deployment)
14. [CI/CD Pipeline](#cicd-pipeline)
15. [Best Practices](#best-practices)

---

## Project Setup & Structure

### Maven Dependencies (pom.xml)

```xml
<?xml version="1.0"?>
<project xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         https://maven.apache.org/xsd/maven-4.0.0.xsd" 
         xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.enterprise</groupId>
    <artifactId>enterprise-quarkus-app</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    
    <properties>
        <compiler-plugin.version>3.11.0</compiler-plugin.version>
        <maven.compiler.release>17</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <quarkus.platform.artifact-id>quarkus-bom</quarkus.platform.artifact-id>
        <quarkus.platform.group-id>io.quarkus.platform</quarkus.platform.group-id>
        <quarkus.platform.version>3.6.4</quarkus.platform.version>
        <skipITs>true</skipITs>
        <surefire-plugin.version>3.0.0</surefire-plugin.version>
    </properties>
    
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>${quarkus.platform.group-id}</groupId>
                <artifactId>${quarkus.platform.artifact-id}</artifactId>
                <version>${quarkus.platform.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
    
    <dependencies>
        <!-- Core Quarkus -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-arc</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-resteasy-reactive-jackson</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-rest-client-reactive-jackson</artifactId>
        </dependency>
        
        <!-- Validation -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-hibernate-validator</artifactId>
        </dependency>
        
        <!-- Database -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-hibernate-orm-panache</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-jdbc-postgresql</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-flyway</artifactId>
        </dependency>
        
        <!-- Security -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-oidc</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-keycloak-authorization</artifactId>
        </dependency>
        
        <!-- Observability -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-micrometer-registry-prometheus</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-opentelemetry</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-smallrye-health</artifactId>
        </dependency>
        
        <!-- Messaging -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-smallrye-reactive-messaging-kafka</artifactId>
        </dependency>
        
        <!-- Caching -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-cache</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-redis-client</artifactId>
        </dependency>
        
        <!-- Cloud Storage -->
        <dependency>
            <groupId>com.azure</groupId>
            <artifactId>azure-storage-blob</artifactId>
            <version>12.25.0</version>
        </dependency>
        <dependency>
            <groupId>com.azure</groupId>
            <artifactId>azure-identity</artifactId>
            <version>1.11.0</version>
        </dependency>
        
        <!-- Resilience -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-smallrye-fault-tolerance</artifactId>
        </dependency>
        
        <!-- Configuration -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-config-yaml</artifactId>
        </dependency>
        
        <!-- Testing -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-junit5</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-junit5-mockito</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>io.rest-assured</groupId>
            <artifactId>rest-assured</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-test-h2</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>postgresql</artifactId>
            <version>1.19.3</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.awaitility</groupId>
            <artifactId>awaitility</artifactId>
            <version>4.2.0</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <plugin>
                <groupId>${quarkus.platform.group-id}</groupId>
                <artifactId>quarkus-maven-plugin</artifactId>
                <version>${quarkus.platform.version}</version>
                <extensions>true</extensions>
                <executions>
                    <execution>
                        <goals>
                            <goal>build</goal>
                            <goal>generate-code</goal>
                            <goal>generate-code-tests</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>${compiler-plugin.version}</version>
                <configuration>
                    <compilerArgs>
                        <arg>-parameters</arg>
                    </compilerArgs>
                </configuration>
            </plugin>
            <plugin>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>${surefire-plugin.version}</version>
                <configuration>
                    <systemPropertyVariables>
                        <java.util.logging.manager>org.jboss.logmanager.LogManager</java.util.logging.manager>
                        <maven.home>${maven.home}</maven.home>
                    </systemPropertyVariables>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

### Project Structure

```
src/
├── main/
│   ├── java/com/enterprise/app/
│   │   ├── api/
│   │   │   ├── resource/              # REST endpoints
│   │   │   ├── dto/                   # Data Transfer Objects
│   │   │   │   ├── request/
│   │   │   │   └── response/
│   │   │   └── mapper/                # DTO mappers
│   │   ├── domain/
│   │   │   ├── entity/                # JPA entities
│   │   │   ├── repository/            # Panache repositories
│   │   │   ├── service/               # Business logic
│   │   │   └── valueobject/           # Domain value objects
│   │   ├── infrastructure/
│   │   │   ├── client/                # External API clients
│   │   │   ├── messaging/             # Kafka producers/consumers
│   │   │   ├── storage/               # Cloud storage services
│   │   │   ├── cache/                 # Caching implementations
│   │   │   └── config/                # Configuration classes
│   │   ├── security/
│   │   │   ├── authentication/
│   │   │   ├── authorization/
│   │   │   └── filter/
│   │   ├── exception/
│   │   │   ├── handler/               # Global exception handlers
│   │   │   └── domain/                # Custom exceptions
│   │   ├── observability/
│   │   │   ├── health/                # Health checks
│   │   │   ├── metrics/               # Custom metrics
│   │   │   └── tracing/               # Tracing configuration
│   │   └── util/                      # Utility classes
│   └── resources/
│       ├── application.yml            # Main configuration
│       ├── application-dev.yml        # Dev profile
│       ├── application-test.yml       # Test profile
│       ├── application-prod.yml       # Production profile
│       ├── db/migration/              # Flyway migrations
│       │   ├── V1__initial_schema.sql
│       │   └── V2__add_audit_fields.sql
│       ├── META-INF/
│       │   └── resources/
│       │       ├── openapi.yml        # OpenAPI specification
│       │       └── banner.txt         # Startup banner
│       └── certificates/              # SSL certificates (if needed)
└── test/
    ├── java/com/enterprise/app/
    │   ├── api/                       # Integration tests
    │   ├── domain/                    # Unit tests
    │   └── infrastructure/            # Infrastructure tests
    └── resources/
        └── application-test.yml
```

---

## Architecture Patterns

### Hexagonal Architecture (Ports & Adapters)

```java
// Domain Layer - Core Business Logic
package com.enterprise.app.domain.service;

import com.enterprise.app.domain.entity.Order;
import com.enterprise.app.domain.repository.OrderRepository;
import com.enterprise.app.domain.port.PaymentPort;
import com.enterprise.app.domain.port.NotificationPort;
import com.enterprise.app.exception.domain.OrderProcessingException;
import io.smallrye.mutiny.Uni;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.transaction.Transactional;
import java.time.Instant;

@ApplicationScoped
public class OrderService {

    @Inject
    OrderRepository orderRepository;

    @Inject
    PaymentPort paymentPort;

    @Inject
    NotificationPort notificationPort;

    @Transactional
    public Order createOrder(Order order) {
        validateOrder(order);
        order.setStatus(Order.OrderStatus.PENDING);
        order.setCreatedAt(Instant.now());
        orderRepository.persist(order);
        return order;
    }

    @Transactional
    public Order processPayment(Long orderId, String paymentToken) {
        Order order = orderRepository.findByIdOptional(orderId)
            .orElseThrow(() -> new OrderProcessingException("Order not found: " + orderId));

        if (order.getStatus() != Order.OrderStatus.PENDING) {
            throw new OrderProcessingException("Order cannot be processed in current status: " + order.getStatus());
        }

        try {
            // Call payment adapter
            PaymentResult result = paymentPort.processPayment(order.getTotalAmount(), paymentToken);
            
            if (result.isSuccess()) {
                order.setStatus(Order.OrderStatus.PAID);
                order.setPaymentReference(result.getTransactionId());
                order.setUpdatedAt(Instant.now());
                
                // Send notification asynchronously
                notificationPort.sendOrderConfirmation(order);
            } else {
                order.setStatus(Order.OrderStatus.PAYMENT_FAILED);
                order.setErrorMessage(result.getErrorMessage());
            }
            
            return order;
        } catch (Exception e) {
            order.setStatus(Order.OrderStatus.PAYMENT_FAILED);
            order.setErrorMessage(e.getMessage());
            throw new OrderProcessingException("Payment processing failed", e);
        }
    }

    private void validateOrder(Order order) {
        if (order.getItems() == null || order.getItems().isEmpty()) {
            throw new OrderProcessingException("Order must contain at least one item");
        }
        if (order.getTotalAmount() == null || order.getTotalAmount().compareTo(BigDecimal.ZERO) <= 0) {
            throw new OrderProcessingException("Order total amount must be greater than zero");
        }
    }
}
```

```java
// Port Interface
package com.enterprise.app.domain.port;

public interface PaymentPort {
    PaymentResult processPayment(BigDecimal amount, String paymentToken);
    PaymentResult refund(String transactionId, BigDecimal amount);
}
```

```java
// Adapter Implementation
package com.enterprise.app.infrastructure.client;

import com.enterprise.app.domain.port.PaymentPort;
import org.eclipse.microprofile.rest.client.inject.RestClient;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;

@ApplicationScoped
public class StripePaymentAdapter implements PaymentPort {

    @Inject
    @RestClient
    StripeApiClient stripeClient;

    @Override
    public PaymentResult processPayment(BigDecimal amount, String paymentToken) {
        try {
            StripePaymentRequest request = new StripePaymentRequest();
            request.setAmount(amount.multiply(new BigDecimal("100")).longValue()); // Convert to cents
            request.setToken(paymentToken);
            request.setCurrency("USD");
            
            StripePaymentResponse response = stripeClient.charge(request);
            
            return PaymentResult.builder()
                .success(response.getStatus().equals("succeeded"))
                .transactionId(response.getId())
                .build();
        } catch (Exception e) {
            return PaymentResult.builder()
                .success(false)
                .errorMessage(e.getMessage())
                .build();
        }
    }

    @Override
    public PaymentResult refund(String transactionId, BigDecimal amount) {
        // Implementation
        return null;
    }
}
```

### Repository Pattern with Panache

```java
package com.enterprise.app.domain.repository;

import com.enterprise.app.domain.entity.Order;
import io.quarkus.hibernate.orm.panache.PanacheRepositoryBase;
import io.quarkus.panache.common.Page;
import io.quarkus.panache.common.Sort;

import javax.enterprise.context.ApplicationScoped;
import java.time.Instant;
import java.util.List;
import java.util.Optional;

@ApplicationScoped
public class OrderRepository implements PanacheRepositoryBase<Order, Long> {

    public List<Order> findByCustomerId(Long customerId, int pageIndex, int pageSize) {
        return find("customerId = ?1", Sort.by("createdAt").descending(), customerId)
            .page(Page.of(pageIndex, pageSize))
            .list();
    }

    public List<Order> findByStatus(Order.OrderStatus status) {
        return list("status", status);
    }

    public List<Order> findOrdersCreatedBetween(Instant startDate, Instant endDate) {
        return list("createdAt between ?1 and ?2", startDate, endDate);
    }

    public Optional<Order> findByOrderNumber(String orderNumber) {
        return find("orderNumber", orderNumber).firstResultOptional();
    }

    public long countByCustomerId(Long customerId) {
        return count("customerId", customerId);
    }

    public List<Order> findPendingOrdersOlderThan(Instant cutoffDate) {
        return list("status = ?1 and createdAt < ?2", Order.OrderStatus.PENDING, cutoffDate);
    }
}
```

### Entity with Auditing

```java
package com.enterprise.app.domain.entity;

import io.quarkus.hibernate.orm.panache.PanacheEntityBase;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import javax.persistence.*;
import java.math.BigDecimal;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "orders", indexes = {
    @Index(name = "idx_order_customer", columnList = "customer_id"),
    @Index(name = "idx_order_status", columnList = "status"),
    @Index(name = "idx_order_number", columnList = "order_number", unique = true)
})
public class Order extends PanacheEntityBase {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "order_number", unique = true, nullable = false, length = 50)
    private String orderNumber;

    @Column(name = "customer_id", nullable = false)
    private Long customerId;

    @Column(name = "total_amount", nullable = false, precision = 19, scale = 2)
    private BigDecimal totalAmount;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 50)
    private OrderStatus status;

    @Column(name = "payment_reference", length = 255)
    private String paymentReference;

    @Column(name = "error_message", length = 1000)
    private String errorMessage;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private Instant updatedAt;

    @Version
    @Column(name = "version")
    private Long version;

    @Column(name = "created_by", length = 100)
    private String createdBy;

    @Column(name = "updated_by", length = 100)
    private String updatedBy;

    public enum OrderStatus {
        PENDING,
        PAID,
        PAYMENT_FAILED,
        SHIPPED,
        DELIVERED,
        CANCELLED
    }

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getOrderNumber() { return orderNumber; }
    public void setOrderNumber(String orderNumber) { this.orderNumber = orderNumber; }

    public Long getCustomerId() { return customerId; }
    public void setCustomerId(Long customerId) { this.customerId = customerId; }

    public BigDecimal getTotalAmount() { return totalAmount; }
    public void setTotalAmount(BigDecimal totalAmount) { this.totalAmount = totalAmount; }

    public OrderStatus getStatus() { return status; }
    public void setStatus(OrderStatus status) { this.status = status; }

    public String getPaymentReference() { return paymentReference; }
    public void setPaymentReference(String paymentReference) { this.paymentReference = paymentReference; }

    public String getErrorMessage() { return errorMessage; }
    public void setErrorMessage(String errorMessage) { this.errorMessage = errorMessage; }

    public List<OrderItem> getItems() { return items; }
    public void setItems(List<OrderItem> items) { this.items = items; }

    public Instant getCreatedAt() { return createdAt; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }

    public Instant getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Instant updatedAt) { this.updatedAt = updatedAt; }

    public Long getVersion() { return version; }
    public void setVersion(Long version) { this.version = version; }

    public String getCreatedBy() { return createdBy; }
    public void setCreatedBy(String createdBy) { this.createdBy = createdBy; }

    public String getUpdatedBy() { return updatedBy; }
    public void setUpdatedBy(String updatedBy) { this.updatedBy = updatedBy; }
}
```

---

## Exception Handling

### Exception Hierarchy

```java
// Base Exception
package com.enterprise.app.exception.domain;

public abstract class ApplicationException extends RuntimeException {
    private final String errorCode;
    private final int httpStatus;

    public ApplicationException(String message, String errorCode, int httpStatus) {
        super(message);
        this.errorCode = errorCode;
        this.httpStatus = httpStatus;
    }

    public ApplicationException(String message, String errorCode, int httpStatus, Throwable cause) {
        super(message, cause);
        this.errorCode = errorCode;
        this.httpStatus = httpStatus;
    }

    public String getErrorCode() {
        return errorCode;
    }

    public int getHttpStatus() {
        return httpStatus;
    }
}
```

```java
// Domain Exceptions
package com.enterprise.app.exception.domain;

import javax.ws.rs.core.Response;

public class OrderProcessingException extends ApplicationException {
    public OrderProcessingException(String message) {
        super(message, "ORDER_PROCESSING_ERROR", Response.Status.BAD_REQUEST.getStatusCode());
    }

    public OrderProcessingException(String message, Throwable cause) {
        super(message, "ORDER_PROCESSING_ERROR", Response.Status.BAD_REQUEST.getStatusCode(), cause);
    }
}

public class ResourceNotFoundException extends ApplicationException {
    public ResourceNotFoundException(String resourceType, String identifier) {
        super(String.format("%s not found with identifier: %s", resourceType, identifier),
              "RESOURCE_NOT_FOUND",
              Response.Status.NOT_FOUND.getStatusCode());
    }
}

public class ExternalServiceException extends ApplicationException {
    public ExternalServiceException(String message, int statusCode) {
        super(message, "EXTERNAL_SERVICE_ERROR", statusCode);
    }

    public ExternalServiceException(String message, Throwable cause) {
        super(message, "EXTERNAL_SERVICE_ERROR", 
              Response.Status.BAD_GATEWAY.getStatusCode(), cause);
    }
}

public class ValidationException extends ApplicationException {
    private final List<ValidationError> validationErrors;

    public ValidationException(String message, List<ValidationError> validationErrors) {
        super(message, "VALIDATION_ERROR", Response.Status.BAD_REQUEST.getStatusCode());
        this.validationErrors = validationErrors;
    }

    public List<ValidationError> getValidationErrors() {
        return validationErrors;
    }

    public static class ValidationError {
        private final String field;
        private final String message;

        public ValidationError(String field, String message) {
            this.field = field;
            this.message = message;
        }

        public String getField() { return field; }
        public String getMessage() { return message; }
    }
}

public class UnauthorizedException extends ApplicationException {
    public UnauthorizedException(String message) {
        super(message, "UNAUTHORIZED", Response.Status.UNAUTHORIZED.getStatusCode());
    }
}

public class ForbiddenException extends ApplicationException {
    public ForbiddenException(String message) {
        super(message, "FORBIDDEN", Response.Status.FORBIDDEN.getStatusCode());
    }
}
```

### Error Response DTO

```java
package com.enterprise.app.api.dto.response;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.Instant;
import java.util.List;
import java.util.Map;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class ErrorResponse {
    private Instant timestamp;
    private int status;
    private String error;
    private String message;
    private String path;
    private String errorCode;
    private String traceId;
    private String spanId;
    private List<FieldError> fieldErrors;
    private Map<String, Object> metadata;

    public ErrorResponse() {
        this.timestamp = Instant.now();
    }

    public static class FieldError {
        private String field;
        private String message;
        private Object rejectedValue;

        public FieldError() {}

        public FieldError(String field, String message) {
            this.field = field;
            this.message = message;
        }

        public FieldError(String field, String message, Object rejectedValue) {
            this.field = field;
            this.message = message;
            this.rejectedValue = rejectedValue;
        }

        // Getters and Setters
        public String getField() { return field; }
        public void setField(String field) { this.field = field; }
        
        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }
        
        public Object getRejectedValue() { return rejectedValue; }
        public void setRejectedValue(Object rejectedValue) { this.rejectedValue = rejectedValue; }
    }

    // Getters and Setters
    public Instant getTimestamp() { return timestamp; }
    public void setTimestamp(Instant timestamp) { this.timestamp = timestamp; }

    public int getStatus() { return status; }
    public void setStatus(int status) { this.status = status; }

    public String getError() { return error; }
    public void setError(String error) { this.error = error; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public String getPath() { return path; }
    public void setPath(String path) { this.path = path; }

    public String getErrorCode() { return errorCode; }
    public void setErrorCode(String errorCode) { this.errorCode = errorCode; }

    public String getTraceId() { return traceId; }
    public void setTraceId(String traceId) { this.traceId = traceId; }

    public String getSpanId() { return spanId; }
    public void setSpanId(String spanId) { this.spanId = spanId; }

    public List<FieldError> getFieldErrors() { return fieldErrors; }
    public void setFieldErrors(List<FieldError> fieldErrors) { this.fieldErrors = fieldErrors; }

    public Map<String, Object> getMetadata() { return metadata; }
    public void setMetadata(Map<String, Object> metadata) { this.metadata = metadata; }
}
```

### Global Exception Handlers

```java
package com.enterprise.app.exception.handler;

import com.enterprise.app.api.dto.response.ErrorResponse;
import com.enterprise.app.exception.domain.*;
import io.opentelemetry.api.trace.Span;
import org.jboss.logging.Logger;

import javax.ws.rs.core.Context;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.UriInfo;
import javax.ws.rs.ext.ExceptionMapper;
import javax.ws.rs.ext.Provider;
import java.util.UUID;
import java.util.stream.Collectors;

@Provider
public class ApplicationExceptionHandler implements ExceptionMapper<ApplicationException> {

    private static final Logger LOG = Logger.getLogger(ApplicationExceptionHandler.class);

    @Context
    UriInfo uriInfo;

    @Override
    public Response toResponse(ApplicationException exception) {
        String traceId = getTraceId();
        String spanId = getSpanId();
        
        logException(exception, traceId);

        ErrorResponse errorResponse = new ErrorResponse();
        errorResponse.setStatus(exception.getHttpStatus());
        errorResponse.setError(Response.Status.fromStatusCode(exception.getHttpStatus()).getReasonPhrase());
        errorResponse.setMessage(exception.getMessage());
        errorResponse.setErrorCode(exception.getErrorCode());
        errorResponse.setPath(uriInfo.getPath());
        errorResponse.setTraceId(traceId);
        errorResponse.setSpanId(spanId);

        // Handle validation errors
        if (exception instanceof ValidationException) {
            ValidationException ve = (ValidationException) exception;
            errorResponse.setFieldErrors(
                ve.getValidationErrors().stream()
                    .map(e -> new ErrorResponse.FieldError(e.getField(), e.getMessage()))
                    .collect(Collectors.toList())
            );
        }

        return Response.status(exception.getHttpStatus())
                .entity(errorResponse)
                .build();
    }

    private void logException(ApplicationException exception, String traceId) {
        if (exception.getHttpStatus() >= 500) {
            LOG.errorf(exception, "[TraceId: %s] Server error occurred", traceId);
        } else {
            LOG.warnf("[TraceId: %s] Client error: %s", traceId, exception.getMessage());
        }
    }

    private String getTraceId() {
        try {
            return Span.current().getSpanContext().getTraceId();
        } catch (Exception e) {
            return UUID.randomUUID().toString();
        }
    }

    private String getSpanId() {
        try {
            return Span.current().getSpanContext().getSpanId();
        } catch (Exception e) {
            return "";
        }
    }
}
```

```java
package com.enterprise.app.exception.handler;

import com.enterprise.app.api.dto.response.ErrorResponse;
import org.jboss.logging.Logger;

import javax.validation.ConstraintViolation;
import javax.validation.ConstraintViolationException;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.UriInfo;
import javax.ws.rs.ext.ExceptionMapper;
import javax.ws.rs.ext.Provider;
import java.util.stream.Collectors;

@Provider
public class ConstraintViolationExceptionHandler 
    implements ExceptionMapper<ConstraintViolationException> {

    private static final Logger LOG = Logger.getLogger(ConstraintViolationExceptionHandler.class);

    @Context
    UriInfo uriInfo;

    @Override
    public Response toResponse(ConstraintViolationException exception) {
        LOG.warnf("Constraint violation: %s", exception.getMessage());

        ErrorResponse errorResponse = new ErrorResponse();
        errorResponse.setStatus(Response.Status.BAD_REQUEST.getStatusCode());
        errorResponse.setError("Bad Request");
        errorResponse.setMessage("Validation failed");
        errorResponse.setErrorCode("VALIDATION_ERROR");
        errorResponse.setPath(uriInfo.getPath());

        errorResponse.setFieldErrors(
            exception.getConstraintViolations().stream()
                .map(this::mapViolation)
                .collect(Collectors.toList())
        );

        return Response.status(Response.Status.BAD_REQUEST)
                .entity(errorResponse)
                .build();
    }

    private ErrorResponse.FieldError mapViolation(ConstraintViolation<?> violation) {
        String field = violation.getPropertyPath().toString();
        String message = violation.getMessage();
        Object rejectedValue = violation.getInvalidValue();
        return new ErrorResponse.FieldError(field, message, rejectedValue);
    }
}
```

```java
package com.enterprise.app.exception.handler;

import com.enterprise.app.api.dto.response.ErrorResponse;
import io.opentelemetry.api.trace.Span;
import org.jboss.logging.Logger;

import javax.ws.rs.core.Context;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.UriInfo;
import javax.ws.rs.ext.ExceptionMapper;
import javax.ws.rs.ext.Provider;
import java.util.UUID;

@Provider
public class GenericExceptionHandler implements ExceptionMapper<Exception> {

    private static final Logger LOG = Logger.getLogger(GenericExceptionHandler.class);

    @Context
    UriInfo uriInfo;

    @Override
    public Response toResponse(Exception exception) {
        String traceId = getTraceId();
        
        LOG.errorf(exception, "[TraceId: %s] Unhandled exception occurred", traceId);

        ErrorResponse errorResponse = new ErrorResponse();
        errorResponse.setStatus(Response.Status.INTERNAL_SERVER_ERROR.getStatusCode());
        errorResponse.setError("Internal Server Error");
        errorResponse.setMessage("An unexpected error occurred. Please contact support with trace ID: " + traceId);
        errorResponse.setErrorCode("INTERNAL_ERROR");
        errorResponse.setPath(uriInfo.getPath());
        errorResponse.setTraceId(traceId);

        return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                .entity(errorResponse)
                .build();
    }

    private String getTraceId() {
        try {
            return Span.current().getSpanContext().getTraceId();
        } catch (Exception e) {
            return UUID.randomUUID().toString();
        }
    }
}
```

---

## Security & Authentication

### JWT/OIDC Configuration

```yaml
# application.yml
quarkus:
  oidc:
    auth-server-url: ${OIDC_AUTH_SERVER_URL:https://keycloak.example.com/realms/enterprise}
    client-id: ${OIDC_CLIENT_ID:enterprise-app}
    credentials:
      secret: ${OIDC_CLIENT_SECRET}
    tls:
      verification: required
    token:
      principal-claim: preferred_username
      issuer: ${OIDC_ISSUER}
    authentication:
      redirect-path: /login
      cookie-path: /
      scopes: openid,profile,email
    roles:
      source: accesstoken
      role-claim-path: realm_access/roles
```

### Security Filter

```java
package com.enterprise.app.security.filter;

import io.quarkus.security.identity.SecurityIdentity;
import org.jboss.logging.Logger;

import javax.inject.Inject;
import javax.ws.rs.container.ContainerRequestContext;
import javax.ws.rs.container.ContainerRequestFilter;
import javax.ws.rs.ext.Provider;
import java.io.IOException;

@Provider
public class SecurityLoggingFilter implements ContainerRequestFilter {

    private static final Logger LOG = Logger.getLogger(SecurityLoggingFilter.class);

    @Inject
    SecurityIdentity securityIdentity;

    @Override
    public void filter(ContainerRequestContext requestContext) throws IOException {
        if (securityIdentity.isAnonymous()) {
            LOG.debugf("Anonymous request to: %s", requestContext.getUriInfo().getPath());
        } else {
            LOG.debugf("Authenticated user '%s' accessing: %s",
                      securityIdentity.getPrincipal().getName(),
                      requestContext.getUriInfo().getPath());
        }
    }
}
```

### Secured REST Endpoint

```java
package com.enterprise.app.api.resource;

import com.enterprise.app.api.dto.request.CreateOrderRequest;
import com.enterprise.app.api.dto.response.OrderResponse;
import com.enterprise.app.domain.service.OrderService;
import io.quarkus.security.Authenticated;
import io.quarkus.security.identity.SecurityIdentity;
import org.eclipse.microprofile.openapi.annotations.Operation;
import org.eclipse.microprofile.openapi.annotations.security.SecurityRequirement;
import org.eclipse.microprofile.openapi.annotations.tags.Tag;

import javax.annotation.security.RolesAllowed;
import javax.inject.Inject;
import javax.validation.Valid;
import javax.ws.rs.*;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.SecurityContext;

@Path("/api/v1/orders")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
@Tag(name = "Orders", description = "Order management operations")
public class OrderResource {

    @Inject
    OrderService orderService;

    @Inject
    SecurityIdentity securityIdentity;

    @POST
    @RolesAllowed({"user", "admin"})
    @Operation(summary = "Create a new order", description = "Creates a new order for the authenticated user")
    @SecurityRequirement(name = "bearerAuth")
    public Response createOrder(@Valid CreateOrderRequest request) {
        String userId = securityIdentity.getPrincipal().getName();
        OrderResponse order = orderService.createOrder(request, userId);
        return Response.status(Response.Status.CREATED).entity(order).build();
    }

    @GET
    @Path("/{orderId}")
    @Authenticated
    @Operation(summary = "Get order by ID")
    @SecurityRequirement(name = "bearerAuth")
    public Response getOrder(@PathParam("orderId") Long orderId) {
        String userId = securityIdentity.getPrincipal().getName();
        OrderResponse order = orderService.getOrder(orderId, userId);
        return Response.ok(order).build();
    }

    @GET
    @RolesAllowed("admin")
    @Operation(summary = "Get all orders (Admin only)")
    @SecurityRequirement(name = "bearerAuth")
    public Response getAllOrders(
            @QueryParam("page") @DefaultValue("0") int page,
            @QueryParam("size") @DefaultValue("20") int size) {
        
        var orders = orderService.getAllOrders(page, size);
        return Response.ok(orders).build();
    }

    @DELETE
    @Path("/{orderId}")
    @RolesAllowed("admin")
    @Operation(summary = "Cancel order (Admin only)")
    @SecurityRequirement(name = "bearerAuth")
    public Response cancelOrder(@PathParam("orderId") Long orderId) {
        orderService.cancelOrder(orderId);
        return Response.noContent().build();
    }
}
```

---

## External API Integration

### REST Client Interface

```java
package com.enterprise.app.infrastructure.client;

import com.enterprise.app.api.dto.request.PaymentRequest;
import com.enterprise.app.api.dto.response.PaymentResponse;
import org.eclipse.microprofile.rest.client.annotation.ClientHeaderParam;
import org.eclipse.microprofile.rest.client.annotation.RegisterClientHeaders;
import org.eclipse.microprofile.rest.client.inject.RegisterRestClient;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;

@Path("/v1/payments")
@RegisterRestClient(configKey = "payment-api")
@RegisterClientHeaders(PaymentApiHeaderFactory.class)
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public interface PaymentApiClient {

    @POST
    @Path("/charge")
    PaymentResponse charge(PaymentRequest request);

    @POST
    @Path("/refund/{transactionId}")
    PaymentResponse refund(
        @PathParam("transactionId") String transactionId,
        @QueryParam("amount") String amount
    );

    @GET
    @Path("/transaction/{transactionId}")
    PaymentResponse getTransaction(@PathParam("transactionId") String transactionId);
}
```

### Client Header Factory

```java
package com.enterprise.app.infrastructure.client;

import org.eclipse.microprofile.config.inject.ConfigProperty;
import org.eclipse.microprofile.rest.client.ext.ClientHeadersFactory;

import javax.enterprise.context.ApplicationScoped;
import javax.ws.rs.core.MultivaluedHashMap;
import javax.ws.rs.core.MultivaluedMap;

@ApplicationScoped
public class PaymentApiHeaderFactory implements ClientHeadersFactory {

    @ConfigProperty(name = "payment-api.api-key")
    String apiKey;

    @Override
    public MultivaluedMap<String, String> update(
            MultivaluedMap<String, String> incomingHeaders,
            MultivaluedMap<String, String> clientOutgoingHeaders) {
        
        MultivaluedMap<String, String> result = new MultivaluedHashMap<>();
        result.add("Authorization", "Bearer " + apiKey);
        result.add("X-API-Version", "2024-01");
        result.add("Content-Type", "application/json");
        return result;
    }
}
```

### REST Client Exception Mapper

```java
package com.enterprise.app.infrastructure.client;

import com.enterprise.app.exception.domain.ExternalServiceException;
import org.eclipse.microprofile.rest.client.ext.ResponseExceptionMapper;
import org.jboss.logging.Logger;

import javax.ws.rs.core.MultivaluedMap;
import javax.ws.rs.core.Response;
import javax.ws.rs.ext.Provider;

@Provider
public class PaymentApiExceptionMapper implements ResponseExceptionMapper<ExternalServiceException> {

    private static final Logger LOG = Logger.getLogger(PaymentApiExceptionMapper.class);

    @Override
    public ExternalServiceException toThrowable(Response response) {
        int status = response.getStatus();
        String message = extractMessage(response);

        LOG.errorf("Payment API error - Status: %d, Message: %s", status, message);

        return new ExternalServiceException(
            String.format("Payment API error (HTTP %d): %s", status, message),
            status
        );
    }

    @Override
    public boolean handles(int status, MultivaluedMap<String, Object> headers) {
        return status >= 400;
    }

    private String extractMessage(Response response) {
        try {
            if (response.hasEntity()) {
                return response.readEntity(String.class);
            }
        } catch (Exception e) {
            LOG.warn("Failed to extract error message from response", e);
        }
        return "Unknown error";
    }
}
```

### Resilience Patterns

```java
package com.enterprise.app.infrastructure.client;

import com.enterprise.app.api.dto.request.PaymentRequest;
import com.enterprise.app.api.dto.response.PaymentResponse;
import com.enterprise.app.domain.port.PaymentPort;
import com.enterprise.app.exception.domain.ExternalServiceException;
import io.smallrye.faulttolerance.api.CircuitBreakerName;
import org.eclipse.microprofile.faulttolerance.*;
import org.eclipse.microprofile.rest.client.inject.RestClient;
import org.jboss.logging.Logger;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import java.time.temporal.ChronoUnit;

@ApplicationScoped
public class ResilientPaymentService implements PaymentPort {

    private static final Logger LOG = Logger.getLogger(ResilientPaymentService.class);

    @Inject
    @RestClient
    PaymentApiClient paymentClient;

    @Retry(
        maxRetries = 3,
        delay = 1000,
        delayUnit = ChronoUnit.MILLIS,
        jitter = 500,
        retryOn = {ExternalServiceException.class}
    )
    @Timeout(value = 5, unit = ChronoUnit.SECONDS)
    @CircuitBreaker(
        requestVolumeThreshold = 10,
        failureRatio = 0.5,
        delay = 30,
        delayUnit = ChronoUnit.SECONDS,
        successThreshold = 2
    )
    @CircuitBreakerName("payment-api-circuit-breaker")
    @Fallback(fallbackMethod = "processPaymentFallback")
    @Bulkhead(value = 10, waitingTaskQueue = 20)
    @Override
    public PaymentResult processPayment(BigDecimal amount, String paymentToken) {
        LOG.debugf("Processing payment: amount=%s", amount);

        try {
            PaymentRequest request = new PaymentRequest();
            request.setAmount(amount);
            request.setToken(paymentToken);
            request.setCurrency("USD");

            PaymentResponse response = paymentClient.charge(request);

            return PaymentResult.builder()
                .success(response.isSuccess())
                .transactionId(response.getTransactionId())
                .errorMessage(response.getErrorMessage())
                .build();

        } catch (Exception e) {
            LOG.errorf(e, "Payment processing failed for amount: %s", amount);
            throw new ExternalServiceException("Payment processing failed", e);
        }
    }

    @SuppressWarnings("unused")
    public PaymentResult processPaymentFallback(BigDecimal amount, String paymentToken) {
        LOG.warnf("Fallback: Payment processing unavailable for amount: %s", amount);
        
        return PaymentResult.builder()
            .success(false)
            .errorMessage("Payment service temporarily unavailable. Please try again later.")
            .build();
    }

    @Override
    @Retry(maxRetries = 2)
    @Timeout(value = 3, unit = ChronoUnit.SECONDS)
    public PaymentResult refund(String transactionId, BigDecimal amount) {
        LOG.debugf("Processing refund: transactionId=%s, amount=%s", transactionId, amount);

        try {
            PaymentResponse response = paymentClient.refund(transactionId, amount.toString());

            return PaymentResult.builder()
                .success(response.isSuccess())
                .transactionId(response.getTransactionId())
                .errorMessage(response.getErrorMessage())
                .build();

        } catch (Exception e) {
            LOG.errorf(e, "Refund failed for transaction: %s", transactionId);
            throw new ExternalServiceException("Refund processing failed", e);
        }
    }
}
```

### SSL/TLS Configuration

```yaml
# application.yml
quarkus:
  rest-client:
    payment-api:
      url: ${PAYMENT_API_URL:https://api.payment-provider.com}
      scope: javax.inject.Singleton
      trust-store: ${TRUSTSTORE_PATH:classpath:certificates/truststore.jks}
      trust-store-password: ${TRUSTSTORE_PASSWORD}
      trust-store-type: JKS
      key-store: ${KEYSTORE_PATH:classpath:certificates/keystore.jks}
      key-store-password: ${KEYSTORE_PASSWORD}
      key-store-type: JKS
      verify-host: true
      connect-timeout: 5000
      read-timeout: 30000
```

---

## Database & Persistence

### Flyway Migration

```sql
-- V1__initial_schema.sql
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    customer_id BIGINT NOT NULL,
    total_amount DECIMAL(19,2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    payment_reference VARCHAR(255),
    error_message VARCHAR(1000),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    version BIGINT NOT NULL DEFAULT 0,
    created_by VARCHAR(100),
    updated_by VARCHAR(100)
);

CREATE INDEX idx_order_customer ON orders(customer_id);
CREATE INDEX idx_order_status ON orders(status);
CREATE INDEX idx_order_created_at ON orders(created_at);

CREATE TABLE order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(19,2) NOT NULL,
    total_price DECIMAL(19,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_order_item_order ON order_items(order_id);
```

```sql
-- V2__add_audit_table.sql
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    entity_type VARCHAR(100) NOT NULL,
    entity_id BIGINT NOT NULL,
    action VARCHAR(50) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    performed_by VARCHAR(100) NOT NULL,
    performed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500)
);

CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_performed_at ON audit_log(performed_at);
CREATE INDEX idx_audit_performed_by ON audit_log(performed_by);
```

### Transaction Management

```java
package com.enterprise.app.domain.service;

import com.enterprise.app.domain.entity.Order;
import com.enterprise.app.domain.entity.AuditLog;
import com.enterprise.app.domain.repository.OrderRepository;
import com.enterprise.app.domain.repository.AuditLogRepository;
import com.enterprise.app.exception.domain.OrderProcessingException;
import org.jboss.logging.Logger;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.transaction.Transactional;
import java.time.Instant;

@ApplicationScoped
public class OrderService {

    private static final Logger LOG = Logger.getLogger(OrderService.class);

    @Inject
    OrderRepository orderRepository;

    @Inject
    AuditLogRepository auditLogRepository;

    @Transactional
    public Order createOrder(CreateOrderRequest request, String userId) {
        LOG.infof("Creating order for user: %s", userId);

        Order order = new Order();
        order.setOrderNumber(generateOrderNumber());
        order.setCustomerId(Long.parseLong(userId));
        order.setTotalAmount(request.getTotalAmount());
        order.setStatus(Order.OrderStatus.PENDING);
        order.setCreatedBy(userId);

        orderRepository.persist(order);

        // Create audit log
        auditLog("ORDER", order.getId(), "CREATE", null, order.toString(), userId);

        LOG.infof("Order created successfully: %s", order.getOrderNumber());
        return order;
    }

    @Transactional
    public void updateOrderStatus(Long orderId, Order.OrderStatus newStatus, String userId) {
        Order order = orderRepository.findByIdOptional(orderId)
            .orElseThrow(() -> new OrderProcessingException("Order not found: " + orderId));

        Order.OrderStatus oldStatus = order.getStatus();
        order.setStatus(newStatus);
        order.setUpdatedBy(userId);
        order.setUpdatedAt(Instant.now());

        // Audit the status change
        auditLog("ORDER", orderId, "UPDATE_STATUS", 
                oldStatus.toString(), newStatus.toString(), userId);

        LOG.infof("Order %s status updated: %s -> %s", orderId, oldStatus, newStatus);
    }

    @Transactional(Transactional.TxType.REQUIRES_NEW)
    protected void auditLog(String entityType, Long entityId, String action, 
                          String oldValue, String newValue, String performedBy) {
        AuditLog audit = new AuditLog();
        audit.setEntityType(entityType);
        audit.setEntityId(entityId);
        audit.setAction(action);
        audit.setOldValue(oldValue);
        audit.setNewValue(newValue);
        audit.setPerformedBy(performedBy);
        audit.setPerformedAt(Instant.now());

        auditLogRepository.persist(audit);
    }

    private String generateOrderNumber() {
        return "ORD-" + Instant.now().toEpochMilli() + "-" + 
               (int)(Math.random() * 10000);
    }
}
```

### Optimistic Locking

```java
@Transactional
public Order updateOrder(Long orderId, UpdateOrderRequest request, Long expectedVersion) {
    Order order = orderRepository.findByIdOptional(orderId)
        .orElseThrow(() -> new ResourceNotFoundException("Order", orderId.toString()));

    // Version check for optimistic locking
    if (!order.getVersion().equals(expectedVersion)) {
        throw new OptimisticLockException(
            "Order has been modified by another transaction. Please refresh and try again.");
    }

    // Update order fields
    order.setTotalAmount(request.getTotalAmount());
    order.setUpdatedAt(Instant.now());

    // Version is automatically incremented by JPA
    return order;
}
```

---

## Messaging & Events

### Kafka Producer

```java
package com.enterprise.app.infrastructure.messaging;

import com.enterprise.app.api.dto.event.OrderCreatedEvent;
import io.smallrye.reactive.messaging.kafka.Record;
import org.eclipse.microprofile.reactive.messaging.Channel;
import org.eclipse.microprofile.reactive.messaging.Emitter;
import org.jboss.logging.Logger;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import java.util.UUID;
import java.util.concurrent.CompletionStage;

@ApplicationScoped
public class OrderEventProducer {

    private static final Logger LOG = Logger.getLogger(OrderEventProducer.class);

    @Inject
    @Channel("order-events")
    Emitter<Record<String, OrderCreatedEvent>> orderEventEmitter;

    public CompletionStage<Void> sendOrderCreatedEvent(OrderCreatedEvent event) {
        String key = event.getOrderId().toString();
        
        LOG.infof("Sending order created event: orderId=%s", event.getOrderId());

        return orderEventEmitter.send(Record.of(key, event))
            .thenRun(() -> LOG.infof("Order event sent successfully: %s", key))
            .exceptionally(throwable -> {
                LOG.errorf(throwable, "Failed to send order event: %s", key);
                return null;
            });
    }
}
```

### Kafka Consumer

```java
package com.enterprise.app.infrastructure.messaging;

import com.enterprise.app.api.dto.event.OrderCreatedEvent;
import com.enterprise.app.domain.service.NotificationService;
import io.smallrye.reactive.messaging.kafka.Record;
import org.eclipse.microprofile.reactive.messaging.Incoming;
import org.jboss.logging.Logger;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import java.util.concurrent.CompletionStage;

@ApplicationScoped
public class OrderEventConsumer {

    private static final Logger LOG = Logger.getLogger(OrderEventConsumer.class);

    @Inject
    NotificationService notificationService;

    @Incoming("order-events")
    public CompletionStage<Void> consume(Record<String, OrderCreatedEvent> record) {
        OrderCreatedEvent event = record.value();
        
        LOG.infof("Received order created event: orderId=%s", event.getOrderId());

        return notificationService.sendOrderConfirmation(event)
            .thenRun(() -> LOG.infof("Order notification sent: %s", event.getOrderId()))
            .exceptionally(throwable -> {
                LOG.errorf(throwable, "Failed to process order event: %s", event.getOrderId());
                // Dead letter queue or retry logic here
                return null;
            });
    }
}
```

### Kafka Configuration

```yaml
# application.yml
mp:
  messaging:
    outgoing:
      order-events:
        connector: smallrye-kafka
        topic: order-events
        key.serializer: org.apache.kafka.common.serialization.StringSerializer
        value.serializer: io.quarkus.kafka.client.serialization.ObjectMapperSerializer
        acks: all
        retries: 3
        max.in.flight.requests.per.connection: 1
        enable.idempotence: true
        compression.type: snappy

    incoming:
      order-events:
        connector: smallrye-kafka
        topic: order-events
        key.deserializer: org.apache.kafka.common.serialization.StringDeserializer
        value.deserializer: io.quarkus.kafka.client.serialization.ObjectMapperDeserializer
        enable.auto.commit: false
        auto.offset.reset: earliest
        group.id: order-processor-group
        failure-strategy: dead-letter-queue
        dead-letter-queue.topic: order-events-dlq
        dead-letter-queue.key.serializer: org.apache.kafka.common.serialization.StringSerializer
        dead-letter-queue.value.serializer: io.quarkus.kafka.client.serialization.ObjectMapperSerializer

kafka:
  bootstrap:
    servers: ${KAFKA_BOOTSTRAP_SERVERS:localhost:9092}
  security:
    protocol: ${KAFKA_SECURITY_PROTOCOL:SASL_SSL}
  sasl:
    mechanism: ${KAFKA_SASL_MECHANISM:PLAIN}
    jaas:
      config: ${KAFKA_JAAS_CONFIG}
```

---

## Caching Strategies

### Cache Configuration

```yaml
# application.yml
quarkus:
  cache:
    caffeine:
      "order-cache":
        initial-capacity: 100
        maximum-size: 1000
        expire-after-write: PT10M
      "product-cache":
        initial-capacity: 500
        maximum-size: 5000
        expire-after-write: PT1H

  redis:
    hosts: ${REDIS_HOST:redis://localhost:6379}
    password: ${REDIS_PASSWORD}
    client-type: standalone
    timeout: 10s
    max-pool-size: 20
```

### Caffeine Cache (In-Memory)

```java
package com.enterprise.app.domain.service;

import com.enterprise.app.domain.entity.Product;
import com.enterprise.app.domain.repository.ProductRepository;
import io.quarkus.cache.CacheResult;
import io.quarkus.cache.CacheInvalidate;
import io.quarkus.cache.CacheInvalidateAll;
import io.quarkus.cache.CacheKey;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;

@ApplicationScoped
public class ProductService {

    @Inject
    ProductRepository productRepository;

    @CacheResult(cacheName = "product-cache")
    public Product getProduct(@CacheKey Long productId) {
        return productRepository.findByIdOptional(productId)
            .orElseThrow(() -> new ResourceNotFoundException("Product", productId.toString()));
    }

    @CacheInvalidate(cacheName = "product-cache")
    public Product updateProduct(@CacheKey Long productId, ProductUpdateRequest request) {
        Product product = productRepository.findById(productId);
        product.setName(request.getName());
        product.setPrice(request.getPrice());
        return product;
    }

    @CacheInvalidateAll(cacheName = "product-cache")
    public void refreshProductCache() {
        // Cache will be cleared
    }
}
```

### Redis Cache (Distributed)

```java
package com.enterprise.app.infrastructure.cache;

import io.quarkus.redis.datasource.RedisDataSource;
import io.quarkus.redis.datasource.value.ValueCommands;
import org.jboss.logging.Logger;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import java.time.Duration;
import java.util.Optional;

@ApplicationScoped
public class RedisCacheService {

    private static final Logger LOG = Logger.getLogger(RedisCacheService.class);

    private final ValueCommands<String, String> commands;

    @Inject
    public RedisCacheService(RedisDataSource ds) {
        this.commands = ds.value(String.class, String.class);
    }

    public void set(String key, String value, Duration ttl) {
        try {
            commands.setex(key, ttl.getSeconds(), value);
            LOG.debugf("Cached value for key: %s", key);
        } catch (Exception e) {
            LOG.errorf(e, "Failed to cache value for key: %s", key);
        }
    }

    public Optional<String> get(String key) {
        try {
            String value = commands.get(key);
            if (value != null) {
                LOG.debugf("Cache hit for key: %s", key);
                return Optional.of(value);
            }
            LOG.debugf("Cache miss for key: %s", key);
            return Optional.empty();
        } catch (Exception e) {
            LOG.errorf(e, "Failed to retrieve cached value for key: %s", key);
            return Optional.empty();
        }
    }

    public void delete(String key) {
        try {
            commands.del(key);
            LOG.debugf("Deleted cache for key: %s", key);
        } catch (Exception e) {
            LOG.errorf(e, "Failed to delete cache for key: %s", key);
        }
    }

    public void deletePattern(String pattern) {
        try {
            // Implementation depends on Redis commands available
            LOG.debugf("Deleted caches matching pattern: %s", pattern);
        } catch (Exception e) {
            LOG.errorf(e, "Failed to delete caches for pattern: %s", pattern);
        }
    }
}
```

---

## Observability & Monitoring

### Health Checks

```java
package com.enterprise.app.observability.health;

import org.eclipse.microprofile.health.HealthCheck;
import org.eclipse.microprofile.health.HealthCheckResponse;
import org.eclipse.microprofile.health.Liveness;
import org.eclipse.microprofile.health.Readiness;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.persistence.EntityManager;

@Liveness
@ApplicationScoped
public class DatabaseLivenessCheck implements HealthCheck {

    @Inject
    EntityManager entityManager;

    @Override
    public HealthCheckResponse call() {
        try {
            entityManager.createNativeQuery("SELECT 1").getSingleResult();
            return HealthCheckResponse.up("Database connection");
        } catch (Exception e) {
            return HealthCheckResponse.down("Database connection");
        }
    }
}

@Readiness
@ApplicationScoped
public class DatabaseReadinessCheck implements HealthCheck {

    @Inject
    EntityManager entityManager;

    @Override
    public HealthCheckResponse call() {
        try {
            // More thorough check for readiness
            entityManager.createQuery("SELECT COUNT(o) FROM Order o").getSingleResult();
            return HealthCheckResponse.up("Database ready");
        } catch (Exception e) {
            return HealthCheckResponse.down("Database not ready");
        }
    }
}

@Readiness
@ApplicationScoped
public class ExternalServiceReadinessCheck implements HealthCheck {

    @Inject
    @RestClient
    PaymentApiClient paymentClient;

    @Override
    public HealthCheckResponse call() {
        try {
            // Ping external service
            paymentClient.getTransaction("health-check");
            return HealthCheckResponse.up("Payment API available");
        } catch (Exception e) {
            return HealthCheckResponse
                .named("Payment API")
                .down()
                .withData("error", e.getMessage())
                .build();
        }
    }
}
```

### Custom Metrics

```java
package com.enterprise.app.observability.metrics;

import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.Timer;
import io.micrometer.core.instrument.Tags;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import java.util.concurrent.Callable;

@ApplicationScoped
public class OrderMetrics {

    private final Counter orderCreatedCounter;
    private final Counter orderProcessedCounter;
    private final Counter orderFailedCounter;
    private final Timer orderProcessingTimer;

    @Inject
    public OrderMetrics(MeterRegistry registry) {
        this.orderCreatedCounter = Counter.builder("orders.created")
            .description("Total number of orders created")
            .register(registry);

        this.orderProcessedCounter = Counter.builder("orders.processed")
            .description("Total number of orders successfully processed")
            .tag("status", "success")
            .register(registry);

        this.orderFailedCounter = Counter.builder("orders.failed")
            .description("Total number of failed orders")
            .tag("status", "failed")
            .register(registry);

        this.orderProcessingTimer = Timer.builder("orders.processing.time")
            .description("Time taken to process orders")
            .register(registry);
    }

    public void incrementOrderCreated() {
        orderCreatedCounter.increment();
    }

    public void incrementOrderProcessed() {
        orderProcessedCounter.increment();
    }

    public void incrementOrderFailed() {
        orderFailedCounter.increment();
    }

    public <T> T recordOrderProcessingTime(Callable<T> callable) throws Exception {
        return orderProcessingTimer.recordCallable(callable);
    }
}
```

### Distributed Tracing

```yaml
# application.yml
quarkus:
  opentelemetry:
    enabled: true
    tracer:
      exporter:
        otlp:
          endpoint: ${OTEL_EXPORTER_OTLP_ENDPOINT:http://jaeger:4317}
      sampler:
        ratio: 1.0  # Sample 100% in dev, reduce in prod
      resource-attributes:
        service.name: ${quarkus.application.name}
        service.version: ${quarkus.application.version}
        deployment.environment: ${ENVIRONMENT:development}
```

```java
package com.enterprise.app.observability.tracing;

import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.context.Context;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;

@ApplicationScoped
public class TracingService {

    @Inject
    Tracer tracer;

    public void addSpanAttribute(String key, String value) {
        Span currentSpan = Span.current();
        currentSpan.setAttribute(key, value);
    }

    public void addEvent(String eventName) {
        Span currentSpan = Span.current();
        currentSpan.addEvent(eventName);
    }

    public <T> T executeInNewSpan(String spanName, java.util.function.Supplier<T> operation) {
        Span span = tracer.spanBuilder(spanName).startSpan();
        try (var scope = span.makeCurrent()) {
            return operation.get();
        } catch (Exception e) {
            span.recordException(e);
            throw e;
        } finally {
            span.end();
        }
    }
}
```

### Logging Configuration

```yaml
# application.yml
quarkus:
  log:
    level: INFO
    category:
      "com.enterprise.app":
        level: DEBUG
    console:
      enable: true
      format: "%d{yyyy-MM-dd HH:mm:ss,SSS} %-5p [%c{3.}] (%t) %s%e%n"
      json: false
    file:
      enable: true
      path: /var/log/quarkus/application.log
      rotation:
        max-file-size: 10M
        max-backup-index: 5
    
    # Structured JSON logging for production
    handler:
      json:
        enable: ${JSON_LOGGING:false}
        
  # OpenTelemetry log correlation
  opentelemetry:
    tracer:
      log-span-id: true
      log-trace-id: true
```

---

## Testing Strategies

### Unit Tests

```java
package com.enterprise.app.domain.service;

import com.enterprise.app.domain.entity.Order;
import com.enterprise.app.domain.repository.OrderRepository;
import com.enterprise.app.exception.domain.OrderProcessingException;
import io.quarkus.test.junit.QuarkusTest;
import io.quarkus.test.junit.mockito.InjectMock;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import javax.inject.Inject;
import java.math.BigDecimal;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@QuarkusTest
class OrderServiceTest {

    @Inject
    OrderService orderService;

    @InjectMock
    OrderRepository orderRepository;

    @Test
    @DisplayName("Should create order successfully")
    void shouldCreateOrderSuccessfully() {
        // Given
        CreateOrderRequest request = new CreateOrderRequest();
        request.setTotalAmount(new BigDecimal("100.00"));
        String userId = "user123";

        // When
        Order result = orderService.createOrder(request, userId);

        // Then
        assertNotNull(result);
        assertEquals(Order.OrderStatus.PENDING, result.getStatus());
        verify(orderRepository, times(1)).persist(any(Order.class));
    }

    @Test
    @DisplayName("Should throw exception when order not found")
    void shouldThrowExceptionWhenOrderNotFound() {
        // Given
        Long orderId = 999L;
        when(orderRepository.findByIdOptional(orderId))
            .thenReturn(Optional.empty());

        // When & Then
        assertThrows(OrderProcessingException.class, () -> {
            orderService.updateOrderStatus(orderId, Order.OrderStatus.PAID, "user123");
        });
    }
}
```

### Integration Tests

```java
package com.enterprise.app.api.resource;

import com.enterprise.app.api.dto.request.CreateOrderRequest;
import io.quarkus.test.junit.QuarkusTest;
import io.quarkus.test.security.TestSecurity;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.CoreMatchers.notNullValue;

@QuarkusTest
class OrderResourceTest {

    @Test
    @TestSecurity(user = "testUser", roles = "user")
    void shouldCreateOrderWhenAuthenticated() {
        CreateOrderRequest request = new CreateOrderRequest();
        request.setTotalAmount(new BigDecimal("150.00"));

        given()
            .contentType(ContentType.JSON)
            .body(request)
        .when()
            .post("/api/v1/orders")
        .then()
            .statusCode(201)
            .body("orderNumber", notNullValue())
            .body("status", is("PENDING"));
    }

    @Test
    void shouldReturnUnauthorizedWhenNotAuthenticated() {
        CreateOrderRequest request = new CreateOrderRequest();
        request.setTotalAmount(new BigDecimal("150.00"));

        given()
            .contentType(ContentType.JSON)
            .body(request)
        .when()
            .post("/api/v1/orders")
        .then()
            .statusCode(401);
    }
}
```

### Test Containers

```java
package com.enterprise.app;

import io.quarkus.test.common.QuarkusTestResourceLifecycleManager;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.containers.KafkaContainer;
import org.testcontainers.utility.DockerImageName;

import java.util.HashMap;
import java.util.Map;

public class TestResources implements QuarkusTestResourceLifecycleManager {

    private static PostgreSQLContainer<?> postgres;
    private static KafkaContainer kafka;

    @Override
    public Map<String, String> start() {
        // Start PostgreSQL
        postgres = new PostgreSQLContainer<>(DockerImageName.parse("postgres:15"))
            .withDatabaseName("test_db")
            .withUsername("test")
            .withPassword("test");
        postgres.start();

        // Start Kafka
        kafka = new KafkaContainer(DockerImageName.parse("confluentinc/cp-kafka:7.5.0"));
        kafka.start();

        Map<String, String> config = new HashMap<>();
        config.put("quarkus.datasource.jdbc.url", postgres.getJdbcUrl());
        config.put("quarkus.datasource.username", postgres.getUsername());
        config.put("quarkus.datasource.password", postgres.getPassword());
        config.put("kafka.bootstrap.servers", kafka.getBootstrapServers());

        return config;
    }

    @Override
    public void stop() {
        if (postgres != null) {
            postgres.stop();
        }
        if (kafka != null) {
            kafka.stop();
        }
    }
}
```

---

## Performance Optimization

### Connection Pooling

```yaml
# application.yml
quarkus:
  datasource:
    jdbc:
      min-size: 5
      max-size: 20
      acquisition-timeout: 10
      idle-removal-interval: PT5M
      leak-detection-interval: PT10M
      transaction-isolation-level: read-committed
      
  hibernate-orm:
    jdbc:
      statement-batch-size: 50
    fetch:
      batch-size: 16
    query:
      query-plan-cache-max-size: 2048
      default-null-ordering: last
```

### Query Optimization

```java
@ApplicationScoped
public class OptimizedOrderRepository implements PanacheRepositoryBase<Order, Long> {

    // Use JOIN FETCH to avoid N+1 queries
    public List<Order> findOrdersWithItems(List<Long> orderIds) {
        return find(
            "SELECT DISTINCT o FROM Order o " +
            "LEFT JOIN FETCH o.items " +
            "WHERE o.id IN ?1",
            orderIds
        ).list();
    }

    // Use pagination for large result sets
    public List<Order> findOrdersPaginated(int page, int size) {
        return find("ORDER BY createdAt DESC")
            .page(Page.of(page, size))
            .list();
    }

    // Use projection for lightweight queries
    @Query("SELECT NEW com.enterprise.app.api.dto.OrderSummary(o.id, o.orderNumber, o.totalAmount) " +
           "FROM Order o WHERE o.customerId = ?1")
    public List<OrderSummary> findOrderSummaries(Long customerId) {
        // Implementation
        return null;
    }
}
```

### Async Processing

```java
@ApplicationScoped
public class AsyncOrderService {

    @Inject
    OrderService orderService;

    @Inject
    ManagedExecutor executor;

    @Asynchronous
    public CompletionStage<Order> processOrderAsync(Long orderId) {
        return CompletableFuture.supplyAsync(() -> {
            return orderService.processOrder(orderId);
        }, executor);
    }
}
```

---

## Configuration Management

### Multi-Environment Configuration

```yaml
# application.yml (Base configuration)
quarkus:
  application:
    name: enterprise-quarkus-app
    version: 1.0.0

  http:
    port: 8080
    cors:
      ~: true
      origins: "*"
      methods: GET,POST,PUT,DELETE
      headers: "*"

  swagger-ui:
    always-include: true
    path: /swagger-ui

---
# application-dev.yml
"%dev":
  quarkus:
    log:
      level: DEBUG
    datasource:
      jdbc:
        url: jdbc:postgresql://localhost:5432/dev_db
    hibernate-orm:
      database:
        generation: drop-and-create

---
# application-test.yml
"%test":
  quarkus:
    datasource:
      jdbc:
        url: jdbc:h2:mem:test_db
    hibernate-orm:
      database:
        generation: drop-and-create

---
# application-prod.yml
"%prod":
  quarkus:
    log:
      level: INFO
      handler:
        json:
          enable: true
    datasource:
      jdbc:
        url: ${DATABASE_URL}
    hibernate-orm:
      database:
        generation: none
      sql-load-script: no-file
```

### Externalized Configuration

```java
package com.enterprise.app.infrastructure.config;

import io.smallrye.config.ConfigMapping;
import io.smallrye.config.WithName;
import io.smallrye.config.WithDefault;

import java.time.Duration;

@ConfigMapping(prefix = "app")
public interface ApplicationConfig {

    @WithName("feature.payment-enabled")
    @WithDefault("true")
    boolean paymentEnabled();

    @WithName("feature.notification-enabled")
    @WithDefault("true")
    boolean notificationEnabled();

    @WithName("order.expiry-duration")
    @WithDefault("PT24H")
    Duration orderExpiryDuration();

    @WithName("order.max-items")
    @WithDefault("100")
    int maxOrderItems();

    PaymentConfig payment();

    interface PaymentConfig {
        @WithName("provider")
        String provider();

        @WithName("timeout")
        @WithDefault("PT30S")
        Duration timeout();

        @WithName("retry-attempts")
        @WithDefault("3")
        int retryAttempts();
    }
}
```

---

## Containerization & Deployment

### Dockerfile (Multi-stage Build)

```dockerfile
## Stage 1: Build
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

## Stage 2: Runtime
FROM registry.access.redhat.com/ubi8/openjdk-17-runtime:latest

ENV LANGUAGE='en_US:en'

# Configure the JAVA_OPTIONS
ENV JAVA_OPTIONS="-Dquarkus.http.host=0.0.0.0 -Djava.util.logging.manager=org.jboss.logmanager.LogManager"

COPY --from=build /app/target/quarkus-app/lib/ /deployments/lib/
COPY --from=build /app/target/quarkus-app/*.jar /deployments/
COPY --from=build /app/target/quarkus-app/app/ /deployments/app/
COPY --from=build /app/target/quarkus-app/quarkus/ /deployments/quarkus/

EXPOSE 8080
USER 185

ENTRYPOINT ["java", "-jar", "/deployments/quarkus-run.jar"]
```

### Kubernetes Deployment

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: enterprise-app
  labels:
    app: enterprise-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: enterprise-app
  template:
    metadata:
      labels:
        app: enterprise-app
    spec:
      containers:
      - name: enterprise-app
        image: enterprise-app:1.0.0
        ports:
        - containerPort: 8080
          protocol: TCP
        env:
        - name: QUARKUS_PROFILE
          value: "prod"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        - name: DATABASE_USERNAME
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: username
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: password
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /q/health/live
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /q/health/ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: enterprise-app-service
spec:
  selector:
    app: enterprise-app
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

### Helm Chart

```yaml
# helm/Chart.yaml
apiVersion: v2
name: enterprise-app
description: Enterprise Quarkus Application
version: 1.0.0
appVersion: "1.0.0"

# helm/values.yaml
replicaCount: 3

image:
  repository: enterprise-app
  pullPolicy: IfNotPresent
  tag: "1.0.0"

service:
  type: LoadBalancer
  port: 80

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
  hosts:
    - host: api.enterprise.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: enterprise-app-tls
      hosts:
        - api.enterprise.com

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

database:
  url: postgresql://postgres:5432/enterprise_db
  username: app_user
  password: changeme
```

---

## CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
          cache: maven
      
      - name: Run tests
        run: mvn test
      
      - name: Generate coverage report
        run: mvn jacoco:report
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG }}
      
      - name: Deploy to Kubernetes
        run: |
          kubectl apply -f kubernetes/
          kubectl rollout status deployment/enterprise-app
```

---

## Best Practices

### 1. **Code Organization**
- Use hexagonal/clean architecture
- Separate domain logic from infrastructure
- Keep controllers thin, services fat
- Use DTOs for API contracts
- Implement proper layering (API → Domain → Infrastructure)

### 2. **Error Handling**
- Create custom exception hierarchy
- Use global exception handlers
- Include trace IDs in error responses
- Log exceptions at appropriate levels
- Provide meaningful error messages

### 3. **Security**
- Use JWT/OIDC for authentication
- Implement proper authorization (RBAC)
- Validate all inputs
- Use parameterized queries (prevent SQL injection)
- Configure CORS properly
- Use HTTPS in production
- Store secrets in environment variables or secret managers

### 4. **Performance**
- Use connection pooling
- Implement caching strategically
- Optimize database queries (avoid N+1)
- Use pagination for large datasets
- Implement async processing where appropriate
- Use bulk operations for batch processing

### 5. **Observability**
- Implement health checks (liveness & readiness)
- Add custom metrics for business KPIs
- Use distributed tracing
- Structure logs properly (JSON in production)
- Monitor external service calls
- Set up alerting for critical errors

### 6. **Testing**
- Write unit tests for business logic
- Write integration tests for APIs
- Use TestContainers for integration tests
- Aim for 80%+ code coverage
- Test error scenarios
- Use meaningful test names

### 7. **Database**
- Use Flyway for schema migrations
- Implement optimistic locking for concurrent updates
- Use proper indexes
- Implement soft deletes where needed
- Use database constraints
- Keep transactions short

### 8. **API Design**
- Follow RESTful principles
- Version your APIs
- Use proper HTTP status codes
- Implement pagination
- Document APIs with OpenAPI/Swagger
- Use DTOs for request/response

### 9. **Configuration**
- Externalize configuration
- Use profiles (dev, test, prod)
- Never commit secrets
- Use ConfigMapping for type-safe config
- Document all configuration options

### 10. **DevOps**
- Use multi-stage Docker builds
- Implement proper CI/CD pipeline
- Use Kubernetes for orchestration
- Implement blue-green or canary deployments
- Monitor application in production
- Set up proper logging aggregation

---

## Common Patterns Summary

### Request Flow
```
Client → REST Controller → Service Layer → Repository → Database
                    ↓
            Exception Handler → Error Response
```

### Dependency Injection
```java
@ApplicationScoped  // Singleton across application
@RequestScoped      // New instance per request
@Inject            // Inject dependencies
```

### Transaction Management
```java
@Transactional                          // Default behavior
@Transactional(REQUIRES_NEW)           // New transaction
@Transactional(REQUIRED)               // Join existing or create
@Transactional(NOT_SUPPORTED)          // Suspend transaction
```

### Async Operations
```java
@Asynchronous
CompletionStage<T> asyncMethod() { ... }
```

### Resilience
```java
@Retry(maxRetries = 3)
@Timeout(value = 5, unit = SECONDS)
@CircuitBreaker(failureRatio = 0.5)
@Fallback(fallbackMethod = "fallbackMethod")
@Bulkhead(value = 10)
```

---

## Conclusion

This skill document provides a comprehensive foundation for building enterprise-grade Quarkus applications. Key takeaways:

1. **Architecture**: Use clean/hexagonal architecture for maintainability
2. **Security**: Implement proper authentication and authorization
3. **Resilience**: Use fault tolerance patterns for external services
4. **Observability**: Implement comprehensive monitoring and tracing
5. **Testing**: Write thorough tests at all levels
6. **Performance**: Optimize database queries and use caching
7. **DevOps**: Automate builds and deployments

Always prioritize:
- Code quality and maintainability
- Security and data protection
- Performance and scalability
- Observability and debugging
- Documentation and knowledge sharing

For production deployments, ensure:
- Proper resource limits
- Health checks configured
- Secrets managed securely
- Monitoring and alerting set up
- Backup and disaster recovery plans
- Regular security updates