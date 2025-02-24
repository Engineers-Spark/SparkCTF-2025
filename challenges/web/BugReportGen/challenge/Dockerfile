
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 5000

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY ["BugReportGen/BugReportGen.csproj","BugReportGen/"]
RUN dotnet restore "BugReportGen/BugReportGen.csproj"

COPY . .
WORKDIR "/src/BugReportGen"
RUN dotnet publish "BugReportGen.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=build /app/publish .
ENV DOTNET_RUNNING_IN_CONTAINER=true
ENV ASPNETCORE_ENVIRONMENT=Production


RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

ENTRYPOINT ["dotnet", "BugReportGen.dll"]
